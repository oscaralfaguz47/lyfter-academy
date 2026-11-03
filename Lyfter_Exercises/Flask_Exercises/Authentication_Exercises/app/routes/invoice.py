from flask import Blueprint, request, url_for
from app.database import get_session

from app.services.purchase_service import PurchaseService
from app.repositories.product_repository import ProductRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.auth import login_required, current_actor
from app.schemas.validation import parse
from app.schemas.invoice import InvoiceListParams, InvoiceRead, PurchaseRequest
from app.routes.responses import pagination_meta
from app.routes.responses import created, ok, serialize, serialize_many


invoices_bp = Blueprint("invoices", __name__, url_prefix="/api/v1/invoices")

def _purchase_service() -> PurchaseService:
    session = get_session()
    return PurchaseService(session, ProductRepository(session), InvoiceRepository(session))

@invoices_bp.post("")
@login_required
def create_invoice():
    data = parse(PurchaseRequest, request.get_json())
    invoice = _purchase_service().purchase(data, current_actor())
    return created(serialize(InvoiceRead, invoice), location=url_for("invoices.get_invoice", invoice_id=invoice.id))

@invoices_bp.get("")
@login_required  # Own invoices, user with Permission.INVOICES_READ sees everyone's 
def list_invoices():
    params = parse(InvoiceListParams, request.args.to_dict(), "Invalid query parameters.")
    invoices, total = _purchase_service().list_invoices(params, current_actor())
    meta = pagination_meta(params.page, params.per_page, total)
    return ok(serialize_many(InvoiceRead, invoices), meta=meta)

@invoices_bp.get("/<int:invoice_id>")
@login_required  # Own invoices, user with Permission.INVOICES_READ sees everyone's 
def get_invoice(invoice_id: int):
    invoice = _purchase_service().get_invoice(invoice_id, current_actor())
    return ok(serialize(InvoiceRead, invoice))