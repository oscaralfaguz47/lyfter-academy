from sqlalchemy import select, Executable, delete, ColumnElement, and_
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert

from decimal import Decimal

from app.models.cart import Cart, CartStatus
from app.models.cart_item import CartItem
from app.errors.exceptions import DomainError, NotFoundError

CONSTRAINT_ERRORS: dict[str, tuple[type[DomainError], str]] = {
    "fk_cart_items_product_id_products": (NotFoundError, "Product not found.")
}

class CartRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_pending_by_user(self, user_id: int) -> Cart | None:
        query = (
            select(Cart)
            .where(_pending_cart_of(user_id))
            .options(selectinload(Cart.cart_items).joinedload(CartItem.product, innerjoin=True))
        )
        return self._session.scalars(query).one_or_none()

    def get_pending_by_user_for_update(self, user_id: int) -> Cart | None:
        """ Load and lock the user's pending cart until commit for the checkout. A second checkout of the same cart waits here. """
        query = (
            select(Cart)
            .where(_pending_cart_of(user_id))
            .options(selectinload(Cart.cart_items)) # selectinload: Postgres can't lock the nullable side of an outer join
            .with_for_update()
        )
        return self._session.scalars(query).one_or_none()
    

    def ensure_pending_cart_id(self, user_id: int) -> int:
        """ Create the user's pending cart if it doesn't exist yet and returns its id. """
        statement = (
            insert(Cart)
            .values(user_id=user_id, status=CartStatus.PENDING)
            .on_conflict_do_nothing(
                index_elements=[Cart.user_id],
                index_where=Cart.status == CartStatus.PENDING,
            )
        )
        self._session.execute(statement)
        query = select(Cart.id).where(_pending_cart_of(user_id))
        return self._session.scalars(query).one()

    def upsert_item(self, cart_id: int, product_id: int, quantity: Decimal) -> None:
        """ Set the quantity of a product, insert the line or overwrite it if it already exists. """
        statement = insert(CartItem).values(cart_id=cart_id, product_id=product_id, quantity=quantity)
        statement = statement.on_conflict_do_update(
            index_elements=[CartItem.cart_id, CartItem.product_id],
            set_={"quantity": statement.excluded.quantity},
        )
        self._execute(statement)

    def delete_item(self, user_id: int, product_id: int) -> bool:
        pending_cart_id = (
            select(Cart.id)
            .where(_pending_cart_of(user_id))
            .scalar_subquery()
        )
        statement = (
            delete(CartItem)
            .where(CartItem.cart_id == pending_cart_id, CartItem.product_id == product_id)
            .returning(CartItem.product_id)
        )
        return self._session.scalars(statement).one_or_none() is not None


    def _execute(self, statement: Executable) -> None:
        try: 
            self._session.execute(statement)
        except IntegrityError as error:
            mapped = CONSTRAINT_ERRORS.get(_violated_constraint(error))
            if mapped is None:
                raise
            error_class, message = mapped
            raise error_class(message) from error

def _pending_cart_of(user_id: int) -> ColumnElement[bool]:
    """ The one condition that identifies a user's open cart, covered by 'uq_carts_user_id_pending'. """
    return and_(Cart.user_id == user_id, Cart.status == CartStatus.PENDING)

def _violated_constraint(error: IntegrityError) -> str | None:
    diagnostics = getattr(error.orig, "diag", None)
    return getattr(diagnostics, "constraint_name", None)
