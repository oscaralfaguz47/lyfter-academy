from sqlalchemy.orm import Session
from sqlalchemy import select, func

from collections.abc import Sequence

from app.models.address import Address

class AddressRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, address_id: int) -> Address | None:
        self._session.get(Address, address_id)

    def list(self, offset: int, limit: int) -> Sequence[Address]:
        query = select(Address).order_by(Address.id).offset(offset).limit(limit)
        return self._session.scalars(query).all()

    def count(self) -> int:
        return self._session.scalar(select(func.count()).select_from(Address)) or 0