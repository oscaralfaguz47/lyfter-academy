from decimal import Decimal
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.invoice_return import InvoiceReturn
from app.models.invoice_return_line import InvoiceReturnLine


class InvoiceReturnRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, invoice_return: InvoiceReturn) -> InvoiceReturn:
        self._session.add(invoice_return)
        self._session.flush()
        return invoice_return

    def returned_quantities(self, invoice_id: int) -> dict[int, Decimal]:
        """ How much of each line of this invoice was already returned: {invoice_line_id: total}. """
        query = (
            select(InvoiceReturnLine.invoice_line_id, func.sum(InvoiceReturnLine.quantity))
            .join(InvoiceReturnLine.invoice_return)
            .where(InvoiceReturn.invoice_id == invoice_id)
            .group_by(InvoiceReturnLine.invoice_line_id)
        )
        return {line_id: total for line_id, total in self._session.execute(query)}

    def list_by_invoice(self, invoice_id: int) -> Sequence[InvoiceReturn]:
        query = (
            select(InvoiceReturn)
            .where(InvoiceReturn.invoice_id == invoice_id)
            .options(selectinload(InvoiceReturn.invoice_return_lines), joinedload(InvoiceReturn.invoice))
            .order_by(InvoiceReturn.id)
        )
        return self._session.scalars(query).all()