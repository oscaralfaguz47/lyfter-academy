from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

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
            .where(Cart.user_id == user_id, Cart.status == CartStatus.PENDING)
            .options(selectinload(Cart.cart_items).joinedload(CartItem.product, innerjoin=True))
        )
        return self._session.scalar(query)

    