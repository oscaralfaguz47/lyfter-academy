
from flask import Blueprint, request

from app.auth import login_required, current_user_id
from app.database import get_session
from app.services.cart_service import CartService
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.routes.responses import ok, serialize
from app.schemas.cart import CartRead, SetCartItemQuantity
from app.schemas.validation import parse


cart_bp = Blueprint("cart", __name__, url_prefix="/api/v1/cart")

def _cart_service() -> CartService:
    session = get_session()
    return CartService(session, CartRepository(session), ProductRepository(session))


@cart_bp.get("")
@login_required
def get_cart():
    cart = _cart_service().get_cart(current_user_id())
    return ok(serialize(CartRead, cart))

@cart_bp.put("/items/<int:product_id>")
@login_required
def set_cart_item(product_id: int):
    data = parse(SetCartItemQuantity, request.get_json())
    cart = _cart_service().set_item(current_user_id(), product_id, data.quantity)
    return ok(serialize(CartRead, cart))