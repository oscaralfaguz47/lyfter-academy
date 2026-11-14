
from sqlalchemy.orm import Session

from app.repositories.cart_repository import CartRepository
from app.schemas.cart import CartRead

class CartService:
    def __init__(self, session: Session, repository: CartRepository) -> None:
        self._session = session
        self._repository = repository


    def get_cart(self, user_id: int) -> CartRead:
        """ The user's pending cart, or an empty one if they don't have it yet, a GET never creates it. """
        cart = self._repository.get_pending_by_user(user_id)
        if cart is None:
            return CartRead(cart_items=[])
        return CartRead.model_validate(cart)

        

    