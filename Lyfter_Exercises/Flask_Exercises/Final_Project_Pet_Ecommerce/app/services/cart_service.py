from decimal import Decimal
import logging

from sqlalchemy.orm import Session

from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.cart import CartRead
from app.errors.exceptions import NotFoundError, ConflictError

logger = logging.getLogger(__name__)

class CartService:
    def __init__(self, session: Session, repository: CartRepository, product_repository: ProductRepository) -> None:
        self._session = session
        self._repository = repository
        self._product_repository = product_repository


    def get_cart(self, user_id: int) -> CartRead:
        """ The user's pending cart, or an empty one if they don't have it yet, a GET never creates it. """
        cart = self._repository.get_pending_by_user(user_id)
        if cart is None:
            return CartRead(cart_items=[])
        return CartRead.model_validate(cart)

    def set_item(self, user_id: int, product_id: int, quantity: Decimal) -> CartRead:
        """ Creates the cart if doesn't exist and upsert its items. """
        product = self._product_repository.get_by_id(product_id)
        if product is None:
            raise NotFoundError(f"Product {product_id} not found.")

        if product.stock < quantity:
            raise ConflictError(
                "Not enough stock.", details={"products": [{"product_id": product_id, "requested": str(quantity), "available": str(product.stock)}]},
            )

        cart_id = self._repository.ensure_pending_cart_id(user_id)
        self._repository.upsert_item(cart_id, product_id, quantity)
        self._session.commit()
        logger.info("User %s set product %s in cart %s, quantity %s", user_id, product_id, cart_id, quantity)

        cart = self._repository.get_pending_by_user(user_id)
        if cart is None:
            raise RuntimeError(f"Pending cart of user {user_id} not found right after upserting an item.")
        return CartRead.model_validate(cart)
