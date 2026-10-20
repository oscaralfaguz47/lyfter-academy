from sqlalchemy.orm import Session

from collections.abc import Sequence
import logging

from app.repositories.vehicle_repository import VehicleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.vehicle_model_repository import VehicleModelRepository
from app.schemas.pagination import PaginationParams
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from app.models.vehicle import Vehicle
from app.errors.exceptions import NotFoundError, ValidationError, ConflictError

logger = logging.getLogger(__name__)

class VehicleService:
    def __init__(self, session: Session, repository: VehicleRepository, user_repository: UserRepository, model_repository: VehicleModelRepository) -> None:
        self._session = session
        self._repository = repository
        self._user_repository = user_repository
        self._model_repository = model_repository

    def list_vehicles(self, pagination: PaginationParams) -> tuple[Sequence[Vehicle], int]:
        vehicles = self._repository.list(offset=pagination.offset, limit=pagination.per_page)
        return vehicles, self._repository.count()

    def create_vehicle(self, data: VehicleCreate) -> Vehicle:
        if self._model_repository.get_by_id(data.model_id) is None:
            raise ValidationError("Invalid vehicle model.", details={"model_id": [f"Model {data.model_id} does not exist."]})
        
        vehicle = self._repository.add(Vehicle(year=data.year, model_id=data.model_id))
        self._session.commit()
        logger.info("Created Vehicle %s", vehicle.id)
        return vehicle

    def get_vehicle(self, vehicle_id: int) -> Vehicle:
        vehicle = self._repository.get_by_id(vehicle_id)
        if vehicle is None: 
            raise NotFoundError(f"Vehicle {vehicle_id} not found.")

        return vehicle

    def update_vehicle(self, vehicle_id: int, data: VehicleUpdate) -> Vehicle:
        vehicle = self.get_vehicle(vehicle_id)
        changes = data.model_dump(exclude_unset=True)

        if "model_id" in changes and self._model_repository.get_by_id(data.model_id) is None:
            raise NotFoundError(f"Vehicle model {data.model_id} not found.")

        for field, value in changes.items():
            setattr(vehicle, field, value)

        self._repository.save(vehicle)
        self._session.commit()
        logger.info("Update vehicle %s (fields: %s)", vehicle.id, ', '.join(changes))
        return vehicle

    def delete_vehicle(self, vehicle_id: int) -> None:
        vehicle = self.get_vehicle(vehicle_id)
        self._repository.delete(vehicle)
        self._session.commit()
        logger.info("Delete vehicle %s", vehicle.id)

    def assign_owner(self, vehicle_id: int, user_id: int) -> Vehicle:
        vehicle = self.get_vehicle(vehicle_id)

        if self._user_repository.get_by_id(user_id) is None:
            raise ValidationError("Invalid owner.", details={"user_id": [f"User {user_id} does not exist."]})

        if vehicle.user_id == user_id:
            return vehicle # It is already assigned

        if vehicle.user_id is not None:
            raise ConflictError(f"Vehicle {vehicle_id} is already assigned to another user.")

        vehicle.user_id = user_id
        self._repository.save(vehicle)
        self._session.commit()
        logger.info("Assigned vehicle %s to user %s", vehicle_id, user_id)
        return self._repository.get_by_id(vehicle_id)

    def remove_owner(self, vehicle_id: int) -> Vehicle:
        vehicle = self.get_vehicle(vehicle_id)
        if vehicle.user_id is not None:
            vehicle.user_id = None
            self._repository.save(vehicle)
            self._session.commit()
            logger.info("Removed owner from vehicle %s", vehicle_id)
        return self.get_vehicle(vehicle_id)