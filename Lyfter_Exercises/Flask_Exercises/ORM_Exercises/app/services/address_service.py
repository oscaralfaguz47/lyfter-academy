
from sqlalchemy.orm import Session

from collections.abc import Sequence

from app.models.address import Address
from app.repositories.address_repository import AddressRepository
from app.schemas.pagination import PaginationParams

class AddressService:
    def __init__(self, session: Session, repository: AddressRepository) -> None:
        self._session = session
        self._repository = repository

    def list_addresses(self, pagination: PaginationParams) ->  tuple[Sequence[Address], int]:
        addresses = self._repository.list(offset=pagination.offset, limit=pagination.per_page)
        return addresses, self._repository.count()
