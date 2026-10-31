import logging
from sqlalchemy.orm import Session

from collections.abc import Sequence

from app.models.address import Address
from app.repositories.address_repository import AddressRepository
from app.repositories.user_repository import UserRepository
from app.schemas.address import AddressCreate, AddressUpdate, AddressListParams
from app.errors.exceptions import NotFoundError, ValidationError

logger = logging.getLogger(__name__)

class AddressService:
    def __init__(self, session: Session, repository: AddressRepository, user_repository: UserRepository) -> None:
        self._session = session
        self._repository = repository
        self._user_repository = user_repository

    def list_addresses(self, params: AddressListParams) ->  tuple[Sequence[Address], int]:
        addresses = self._repository.list(params)
        return addresses, self._repository.count(params)

    def create_address(self, data: AddressCreate) -> Address:
        if self._user_repository.get_by_id(data.user_id) is None:
            raise ValidationError("Invalid user.", details={"user_id": [f"User {data.user_id} does not exist."]})
        
        address = self._repository.add(
            Address(
                line1=data.line1, 
                line2=data.line2, 
                city=data.city, 
                state=data.state, 
                zip_code=data.zip_code,
                user_id=data.user_id
                )
            )
        
        self._session.commit()
        logger.info("Created address %s", address.id)
        return address

    def get_address(self, address_id: int) -> Address:
        address = self._repository.get_by_id(address_id)
        if address is None:
            raise NotFoundError(f"Address {address_id} not found.")
        return address

    def update_address(self, address_id: int, data: AddressUpdate) -> Address:
        address = self.get_address(address_id)
        changes = data.model_dump(exclude_unset=True)

        for field, value in changes.items():
            setattr(address, field, value)

        self._repository.save(address)
        self._session.commit()
        logger.info("Update address %s (fields: %s)", address.id, ", ".join(changes))
        return address

    def delete_address(self, address_id: int) -> None:
        address = self.get_address(address_id)

        self._repository.delete(address)
        self._session.commit()
        logger.info("Delete address %s", address_id)