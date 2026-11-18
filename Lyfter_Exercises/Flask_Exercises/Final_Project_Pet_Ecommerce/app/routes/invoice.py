from flask import Blueprint, request, url_for

from app.auth import current_actor, login_required, permission_required
from app.cache import get_cache
from app.database import get_session
from app.repositories.cart_repository import CartRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.invoice_return_repository import InvoiceReturnRepository
from app.repositories.product_cache import ProductCache
from app.repositories.product_repository import ProductRepository
from app.repositories.invoice_cache import InvoiceCache
from app.routes.responses import created, ok, pagination_meta, serialize, serialize_many
from app.schemas.invoice import InvoiceListParams, InvoiceRead, InvoiceUpdate
from app.schemas.invoice_return import InvoiceReturnRead, InvoiceReturnRequest
from app.schemas.validation import parse
from app.security.permissions import Permission
from app.services.purchase_service import PurchaseService
from app.services.return_service import ReturnService



invoices_bp = Blueprint("invoices", __name__, url_prefix="/api/v1/invoices")

def purchase_service() -> PurchaseService:
    """ Build the service for this request. Public because the cart's checkout route uses it too. """
    session = get_session()
    return PurchaseService(
        session, 
        ProductRepository(session), 
        InvoiceRepository(session), 
        CartRepository(session), 
        ProductCache(get_cache()),
        InvoiceCache(get_cache()),
    )

def _return_service() -> ReturnService:
    session = get_session()
    return ReturnService(
        session, 
        InvoiceRepository(session), 
        InvoiceReturnRepository(session), 
        ProductRepository(session), 
        ProductCache(get_cache()),
        InvoiceCache(get_cache()),
    )

# Invoices are created only through POST /cart/checkout

@invoices_bp.get("")
@login_required  # Own invoices, user with Permission.INVOICES_READ sees everyone's
def list_invoices():
    params = parse(InvoiceListParams, request.args.to_dict(), "Invalid query parameters.")
    invoices, total = purchase_service().list_invoices(params, current_actor())
    meta = pagination_meta(params.page, params.per_page, total)
    return ok(serialize_many(InvoiceRead, invoices), meta=meta)

@invoices_bp.get("/<int:invoice_number>")
@login_required  # Own invoices, user with Permission.INVOICES_READ sees everyone's
def get_invoice(invoice_number: int):
    invoice = purchase_service().get_invoice(invoice_number, current_actor())
    return ok(serialize(InvoiceRead, invoice))

@invoices_bp.patch("/<int:invoice_number>")
@permission_required(Permission.INVOICES_UPDATE)
def update_invoice(invoice_number: int):
    data = parse(InvoiceUpdate, request.get_json())
    invoice = purchase_service().update_billing(invoice_number, data, current_actor())
    return ok(serialize(InvoiceRead, invoice))

@invoices_bp.post("/<int:invoice_number>/returns")
@permission_required(Permission.INVOICES_RETURN)
def create_return(invoice_number: int):
    data = parse(InvoiceReturnRequest, request.get_json())
    invoice_return = _return_service().create_return(invoice_number, data, current_actor())
    return created(serialize(InvoiceReturnRead, invoice_return), location=url_for("invoices.list_returns", invoice_number=invoice_number))

@invoices_bp.get("/<int:invoice_number>/returns")
@login_required  # Own invoices, user with Permission.INVOICES_READ sees everyone's
def list_returns(invoice_number: int):
    returns = _return_service().list_returns(invoice_number, current_actor())
    return ok(serialize_many(InvoiceReturnRead, returns))