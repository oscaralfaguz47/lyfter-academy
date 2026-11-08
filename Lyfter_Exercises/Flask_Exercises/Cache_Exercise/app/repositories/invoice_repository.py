from sqlalchemy import select, Select, func
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError
from collections.abc import Sequence

from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceListParams
from app.errors.exceptions import NotFoundError, DomainError, ValidationError, ConflictError

SORT_COLUMNS = {"id": Invoice.id, "invoice_number": Invoice.invoice_number}
CONSTRAINT_ERRORS: dict[str, tuple[type[DomainError], str]] = {
    "fk_invoices_client_id_users": (NotFoundError, "User (client_id) not found."),
    "fk_invoice_lines_product_id_products": (ValidationError, "Some products don't exist."),
    "uq_invoice_lines_invoice_id": (ConflictError, "Each product can appear only once per invoice."),
}

class InvoiceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, invoice: Invoice) -> Invoice:
        self._session.add(invoice)
        self._flush()
        return invoice

    def get_by_id(self, invoice_id: int) -> Invoice | None:
        query = select(Invoice).where(Invoice.id == invoice_id).options(selectinload(Invoice.invoice_lines))
        return self._session.scalar(query)

    def list(self, params: InvoiceListParams, client_id: int | None = None) -> Sequence[Invoice]:
        query = (
            self._filtered(params, client_id)
            .options(selectinload(Invoice.invoice_lines))
            .order_by(*_sort_clauses(params.sort))
            .offset(params.offset)
            .limit(params.per_page)
        )
        return self._session.scalars(query).all()

    def count(self, params: InvoiceListParams, client_id: int | None = None) -> int:
        query = self._filtered(params, client_id).with_only_columns(func.count(Invoice.id))
        return self._session.scalar(query) or 0


    def _flush(self) -> None:
        try:
            self._session.flush()
        except IntegrityError as error:
            mapped = CONSTRAINT_ERRORS.get(_violated_constraint(error))
            if mapped is None:
                raise
            error_class, message = mapped
            raise error_class(message) from error

    def _filtered(self, params: InvoiceListParams, client_id: int | None) -> Select:
        query = select(Invoice)
        if client_id is not None:
            query = query.where(Invoice.client_id == client_id)
        if params.invoice_number is not None:
            query = query.where(Invoice.invoice_number == params.invoice_number)
        return query


def _violated_constraint(error: IntegrityError) -> str | None:
    diagnostics = getattr(error.orig, "diag", None)
    return getattr(diagnostics, "constraint_name", None)

def _sort_clauses(sort: str) -> tuple:
    column = SORT_COLUMNS[sort.lstrip("-")]
    return (column.desc() if sort.startswith("-") else column.asc(), Invoice.id)