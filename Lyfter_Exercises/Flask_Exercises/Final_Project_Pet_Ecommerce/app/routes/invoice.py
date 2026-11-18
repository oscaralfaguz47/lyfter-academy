from flask import Blueprint, request
from app.database import get_session

from app.services.purchase_service import PurchaseService
from app.repositories.product_repository import ProductRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.product_cache import ProductCache
from app.repositories.cart_repository import CartRepository
from app.auth import login_required, current_actor
from app.schemas.validation import parse
from app.schemas.invoice import InvoiceListParams, InvoiceRead
from app.routes.responses import pagination_meta
from app.routes.responses import ok, serialize, serialize_many
from app.cache import get_cache


invoices_bp = Blueprint("invoices", __name__, url_prefix="/api/v1/invoices")

def purchase_service() -> PurchaseService:
    """ Build the service for this request. Public because the cart's checkout route uses it too. """
    session = get_session()
    return PurchaseService(
        session, ProductRepository(session), InvoiceRepository(session), CartRepository(session), ProductCache(get_cache())
    )

# Invoices are created only through POST /cart/checkout

@invoices_bp.get("")
@login_required  # Own invoices, user with Permission.INVOICES_READ sees everyone's 
def list_invoices():
    params = parse(InvoiceListParams, request.args.to_dict(), "Invalid query parameters.")
    invoices, total = purchase_service().list_invoices(params, current_actor())
    meta = pagination_meta(params.page, params.per_page, total)
    return ok(serialize_many(InvoiceRead, invoices), meta=meta)

@invoices_bp.get("/<int:invoice_id>")
@login_required  # Own invoices, user with Permission.INVOICES_READ sees everyone's 
def get_invoice(invoice_id: int):
    invoice = purchase_service().get_invoice(invoice_id, current_actor())
    return ok(serialize(InvoiceRead, invoice))