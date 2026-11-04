
from sqlalchemy import select, Select, or_, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from collections.abc import Sequence

from app.models.contact import Contact
from app.errors.exceptions import ConflictError, DomainError, NotFoundError
from app.schemas.contact import ContactListParams

SORT_COLUMNS = {"id": Contact.id, "name": Contact.name}
CONSTRAINT_ERRORS: dict[str, tuple[type[DomainError], str]] = {
    "uq_contacts_email": (ConflictError,"The email can appear only once, the attempted to save already exists."),
    "uq_contacts_phone": (ConflictError, "The phone can appear only once the attempted to save already exists."),
    "fk_contacts_user_id_users": (NotFoundError, "User not found."),
}
SEARCHABLE_COLUMNS = {"name", "email", "phone"}

class ContactRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, contact: Contact) -> Contact:
        self._session.add(contact)
        self._flush()
        return contact

    def get_by_id(self, contact_id: int) -> Contact | None:
        query = select(Contact).where(Contact.id == contact_id)
        return self._session.scalar(query)

    def list(self, params: ContactListParams, user_id: int | None = None) -> Sequence[Contact]:
        query = (
            self._filtered(params, user_id)
            .order_by(*_sort_clauses(params.sort))
            .offset(params.offset)
            .limit(params.per_page)
        )
        return self._session.scalars(query).all()

    def count(self, params: ContactListParams, user_id: int | None = None) -> int:
        query = self._filtered(params, user_id).with_only_columns(func.count(Contact.id))
        return self._session.scalar(query) or 0

    def save(self, contact: Contact) -> Contact:
        self._flush()
        return contact

    def delete(self, contact: Contact) -> None:
        self._session.delete(contact)
        self._flush()

    def _filtered(self, params: ContactListParams, user_id: int | None = None) -> Select:
        query = select(Contact)
        if user_id is not None:
            query = query.where(Contact.user_id == user_id)
        if params.search is not None:
            query = query.where(
                or_(*(column.icontains(params.search, autoescape=True) for column in SEARCHABLE_COLUMNS))
            )
        return query

    def _flush(self) -> None:
        try:
            self._session.flush()
        except IntegrityError as error:
            mapped = CONSTRAINT_ERRORS.get(_violated_constraint(error))
            if mapped is None: 
                raise
            error_class, message = mapped
            raise error_class(message) from error


def _violated_constraint(error: IntegrityError) -> str | None:
    diagnostics = getattr(error.orig, "diag", None)
    return getattr(diagnostics, "constraint_name", None)

def _sort_clauses(sort: str) -> tuple:
    column = SORT_COLUMNS[sort.lstrip("-")]
    return (column.desc() if sort.startswith("-") else column.asc(), Contact.id)