from sqlalchemy.orm import Session
from decimal import Decimal, ROUND_HALF_UP
from collections.abc import Sequence
from app.errors.exceptions import ConflictError, ValidationError, NotFoundError

import logging
logger = logging.getLogger(__name__)


from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.invoice import PurchaseRequest, InvoiceListParams
from app.security.permissions import Actor, Permission
from app.models.invoice import Invoice
from app.models.invoice_line import InvoiceLine
from app.models.product import Product

CENTS = Decimal("0.01")


class PurchaseService:
    def __init__(self, session: Session, product_repository: ProductRepository, invoice_repository: InvoiceRepository) -> None:
        self._product_repository = product_repository
        self._invoice_repository = invoice_repository
        self._session = session

    def purchase(self, data: PurchaseRequest, actor: Actor) -> Invoice:
        quantities = {item.product_id: item.quantity for item in data.items}

        # Load and lock every product.
        products = self._product_repository.get_many_for_updates(list(quantities))
        _ensure_all_exist(quantities, products)
        _ensure_enough_stock(quantities, products)

        # Build the invoice with prices from the database.
        invoice = Invoice(client_id=actor.id, total_amount=Decimal(0), created_by_id=actor.id)
        for product in products:
            quantity = quantities[product.id]
            line_total = (product.price * quantity).quantize(CENTS, rounding=ROUND_HALF_UP)
            invoice.invoice_lines.append(
                InvoiceLine(product_id=product.id, quantity=quantity, price=product.price, total_amount=line_total)
            )
            invoice.total_amount += line_total
            product.stock -= quantity
        # One commit for everything, invoice, invoice_lines and product.stock
        self._invoice_repository.add(invoice)
        self._session.commit()
        logger.info("User %s bought %s products (invoice %s, total %s)", actor.id, len(products), invoice.id, invoice.total_amount)
        return invoice

    def get_invoice(self, invoice_id: int, actor: Actor) -> Invoice:
        invoice = self._invoice_repository.get_by_id(invoice_id)
        if invoice is None or (invoice.client_id != actor.id and not actor.can(Permission.INVOICES_READ)):
            raise NotFoundError(f"Invoice {invoice_id} not found.")
        return invoice

    def list_invoices(self, params: InvoiceListParams, actor: Actor) -> tuple[Sequence[Invoice], int]:
        client_id = params.client_id if actor.can(Permission.INVOICES_READ) else actor.id  # The user sees their own invoices and Admin sees all
        invoices = self._invoice_repository.list(params, client_id)
        return invoices, self._invoice_repository.count(params, client_id)



def _ensure_all_exist(quantities: dict[int, Decimal], products: Sequence[Product]) -> None:
    missing = sorted(set(quantities) - {product.id for product in products})
    if missing: 
        raise ValidationError("Some products don't exist.", details={"product_ids": missing})

def _ensure_enough_stock(quantities: dict[int, Decimal], products: Sequence[Product]) -> None:
    short = [
        {"product_id": p.id, "requested": str(quantities[p.id]), "available": str(p.stock)}
        for p in products
        if p.stock < quantities[p.id]
    ]
    if short:
        raise ConflictError("Not enough stock.", details={"products": short})