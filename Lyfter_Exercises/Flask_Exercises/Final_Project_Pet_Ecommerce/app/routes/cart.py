
from flask import Blueprint, request, url_for

from app.auth import login_required, current_user_id, current_actor
from app.database import get_session
from app.services.cart_service import CartService
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.routes.responses import ok, serialize, created
from app.schemas.cart import CartRead, SetCartItemQuantity
from app.schemas.validation import parse
from app.schemas.invoice import CheckoutRequest, InvoiceRead
from app.routes.invoice import purchase_service


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

@cart_bp.delete("/items/<int:product_id>")
@login_required
def remove_cart_item(product_id: int):
    cart = _cart_service().remove_item(current_user_id(), product_id)
    return ok(serialize(CartRead, cart))

@cart_bp.post("/checkout")
@login_required
def checkout():
    data = parse(CheckoutRequest, request.get_json())
    invoice = purchase_service().checkout(data, current_actor())
    return created(serialize(InvoiceRead, invoice), location=url_for("invoices.get_invoice", invoice_id=invoice.id))