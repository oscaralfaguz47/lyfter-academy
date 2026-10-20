from sqlalchemy.orm import Session, contains_eager
from sqlalchemy import select, func, Select
from sqlalchemy.exc import IntegrityError

from collections.abc import Sequence

from app.models.vehicle import Vehicle
from app.models.vehicle_model import VehicleModel
from app.errors.exceptions import NotFoundError

class VehicleRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list(self, offset: int, limit: int) -> Sequence[Vehicle]:
        query = (
            self._with_model_and_brand()
            .options(contains_eager(Vehicle.vehicle_model).contains_eager(VehicleModel.brand))
            .order_by(Vehicle.id)
            .offset(offset)
            .limit(limit)
        )
        return self._session.scalars(query).all()

    def count(self) -> int:
        query = self._with_model_and_brand().with_only_columns(func.count(Vehicle.id))
        return self._session.scalar(query) or 0

    def add(self, vehicle: Vehicle) -> Vehicle:
        self._session.add(vehicle)
        self._flush()
        return vehicle

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        return self._session.get(Vehicle, vehicle_id)

    def save(self, vehicle: Vehicle) -> Vehicle:
        self._flush()
        return vehicle

    def delete(self, vehicle: Vehicle) -> None:
        self._session.delete(vehicle)
        self._session.flush()

    # The joins shared by list() and count(), so the filter applies to both
    @staticmethod
    def _with_model_and_brand() -> Select:
        return select(Vehicle).join(Vehicle.vehicle_model).join(VehicleModel.brand)

    def _flush(self) -> None:
        try:
            self._session.flush()
        except IntegrityError as error:
            constraint = _violated_constraint(error)
            if constraint == "fk_vehicles_model_id_vehicle_models":
                raise NotFoundError("Vehicle model not found.") from error
            if constraint == "fk_vehicles_user_id_users": 
                raise NotFoundError("User not found.") from error
            raise


def _violated_constraint(error: IntegrityError) -> str | None:
    diagnostics = getattr(error.orig, "diag", None)
    return getattr(diagnostics, "constraint_name", None)