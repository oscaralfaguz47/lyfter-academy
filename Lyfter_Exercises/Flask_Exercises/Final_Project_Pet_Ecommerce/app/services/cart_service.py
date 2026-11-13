
from sqlalchemy.orm import Session

from app.repositories.cart_repository import CartRepository
from app.models.cart import Cart

class CartService:
    def __init__(self, session: Session, repository: CartRepository) -> None:
        self._session = session
        self._repository = repository


    def get_cart(self, user_id: int) -> Cart:
        cart = self._repository.get_pending_by_user(user_id)
        if cart:
            return cart
        else: 
            return Cart() 

        

    