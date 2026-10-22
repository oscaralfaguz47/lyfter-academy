from sqlalchemy.orm import Session
from sqlalchemy import select, func

from collections.abc import Sequence

from app.models.address import Address

class AddressRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list(self, offset: int, limit: int) -> Sequence[Address]:
        query = select(Address).order_by(Address.id).offset(offset).limit(limit)
        return self._session.scalars(query).all()

    def count(self) -> int:
        return self._session.scalar(select(func.count()).select_from(Address)) or 0

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


    def _flush(self) -> None:
        self._session.flush()