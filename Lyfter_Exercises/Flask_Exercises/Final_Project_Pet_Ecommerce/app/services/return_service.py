import logging
from collections.abc import Sequence
from decimal import Decimal

from sqlalchemy.orm import Session

from app.domain.pricing import line_total
from app.errors.exceptions import ConflictError, NotFoundError, ValidationError
from app.models.invoice import InvoiceStatus
from app.models.invoice_line import InvoiceLine
from app.models.invoice_return import InvoiceReturn
from app.models.invoice_return_line import InvoiceReturnLine
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.invoice_return_repository import InvoiceReturnRepository
from app.repositories.product_cache import ProductCache
from app.repositories.product_repository import ProductRepository
from app.schemas.invoice_return import InvoiceReturnRequest
from app.security.permissions import Actor, Permission

logger = logging.getLogger(__name__)



class ReturnService:
    def __init__(
            self,
            session: Session,
            invoice_repository: InvoiceRepository,
            return_repository: InvoiceReturnRepository,
            product_repository: ProductRepository,
            product_cache: ProductCache,
            ) -> None:
        self._session = session
        self._invoice_repository = invoice_repository
        self._return_repository = return_repository
        self._product_repository = product_repository
        self._product_cache = product_cache

    def create_return(self, invoice_number: int, data: InvoiceReturnRequest, actor: Actor) -> InvoiceReturn:
        """ Return some or all of an invoice's lines: restore the stock and refund the frozen prices, in one transaction. """
        invoice = self._invoice_repository.get_by_number_for_update(invoice_number)
        if invoice is None:
            raise NotFoundError(f"Invoice {invoice_number} not found.")
        if invoice.status == InvoiceStatus.RETURNED:
            raise ConflictError(f"Invoice {invoice_number} is already returned.")

        requested = {line.invoice_line_id: line.quantity for line in data.lines}
        lines = {line.id: line for line in invoice.invoice_lines}
        _ensure_lines_belong_to_invoice(requested, lines, invoice_number)
        returned = self._return_repository.returned_quantities(invoice.id)
        _ensure_enough_left(requested, lines, returned)

        products = self._product_repository.get_many_for_updates([lines[line_id].product_id for line_id in requested])
        products_by_id = {product.id: product for product in products}

        invoice_return = InvoiceReturn(invoice=invoice, reason=data.reason, refund_amount=Decimal(0), created_by_id=actor.id)
        for line_id, quantity in requested.items():
            line = lines[line_id]
            products_by_id[line.product_id].stock += quantity
            invoice_return.refund_amount += line_total(line.price, quantity)  # The price frozen at the sale, not today's
            invoice_return.invoice_return_lines.append(InvoiceReturnLine(invoice_line_id=line_id, quantity=quantity))
        if _fully_returned(invoice.invoice_lines, returned, requested):
            invoice.status = InvoiceStatus.RETURNED

        self._return_repository.add(invoice_return)
        self._session.commit()  # One commit: the return, its lines, the stock and the invoice status
        self._product_cache.invalidate(*products_by_id)
        logger.info("User %s returned %s lines of invoice %s (refund %s)", actor.id, len(requested), invoice_number, invoice_return.refund_amount)
        return invoice_return

    def list_returns(self, invoice_number: int, actor: Actor) -> Sequence[InvoiceReturn]:
        """ The owner or an admin; someone else's invoice returns the same 404 as a missing one. """
        invoice = self._invoice_repository.get_by_number(invoice_number)
        if invoice is None or not actor.can_access_user(invoice.client_id, Permission.INVOICES_READ):
            raise NotFoundError(f"Invoice {invoice_number} not found.")
        return self._return_repository.list_by_invoice(invoice.id)


def _ensure_lines_belong_to_invoice(requested: dict[int, Decimal], lines: dict[int, InvoiceLine], invoice_number: int) -> None:
    foreign = sorted(set(requested) - set(lines))
    if foreign:
        raise ValidationError(f"Some lines don't belong to invoice {invoice_number}.", details={"invoice_line_ids": foreign})


def _ensure_enough_left(requested: dict[int, Decimal], lines: dict[int, InvoiceLine], returned: dict[int, Decimal]) -> None:
    short = []
    for line_id, quantity in requested.items():
        left = lines[line_id].quantity - returned.get(line_id, Decimal(0))
        if quantity > left:
            short.append({"invoice_line_id": line_id, "requested": str(quantity), "available": str(left)})
    if short:
        raise ConflictError("Not enough left to return.", details={"lines": short})


def _fully_returned(lines: Sequence[InvoiceLine], returned: dict[int, Decimal], requested: dict[int, Decimal]) -> bool:
    return all(returned.get(line.id, Decimal(0)) + requested.get(line.id, Decimal(0)) >= line.quantity for line in lines)