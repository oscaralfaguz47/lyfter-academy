from sqlalchemy.orm import Session

from collections.abc import Sequence

from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.pagination import PaginationParams
from app.models.vehicle import Vehicle

class VehicleService:
    def __init__(self, session: Session, repository: VehicleRepository) -> None:
        self._session = session
        self._repository = repository

    def list_vehicles(self, pagination: PaginationParams) -> tuple[Sequence[Vehicle], int]:
        vehicles = self._repository.list(offset=pagination.offset, limit=pagination.per_page)
        return vehicles, self._repository.count()