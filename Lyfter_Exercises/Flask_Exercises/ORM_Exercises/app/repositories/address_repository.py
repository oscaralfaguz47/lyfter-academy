from sqlalchemy.orm import Session
from sqlalchemy import select, func, Select, or_

from collections.abc import Sequence

from app.models.address import Address
from app.schemas.address import AddressListParams

SEARCHABLE_COLUMNS = (Address.line1, Address.line2)
SORT_COLUMNS = {"id": Address.id}

class AddressRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list(self, params: AddressListParams) -> Sequence[Address]:
        query = self._filtered(params).order_by(*_sort_clauses(params.sort)).offset(params.offset).limit(params.per_page)
        return self._session.scalars(query).all()

    def count(self, params: AddressListParams) -> int:
        query = self._filtered(params).with_only_columns(func.count(Address.id))
        return self._session.scalar(query) or 0

    def add(self, address: Address) -> Address:
        self._session.add(address)
        self._flush()
        return address

    def get_by_id(self, address_id: int) -> Address | None:
        return self._session.get(Address, address_id)

    def save(self, address: Address) -> Address:
        self._flush()
        return address

    def delete(self, address: Address) -> None:
        self._session.delete(address)
        self._session.flush()

    def _filtered(self, params: AddressListParams) -> Select:
        query = select(Address)
        if params.search is not None:
            query = query.where(
                or_(*(column.icontains(params.search, autoescape=True) for column in SEARCHABLE_COLUMNS))
            )
        return query


    def _flush(self) -> None:
        self._session.flush()

def _sort_clauses(sort: str) -> tuple:
    column = SORT_COLUMNS[sort.lstrip("-")]
    return (column.desc() if sort.startswith("-") else column.asc(), Address.id)