from sqlalchemy.orm import Session, contains_eager
from sqlalchemy import select, func, Select
from sqlalchemy.exc import IntegrityError

from collections.abc import Sequence

from app.models import Vehicle, VehicleModel
from app.errors.exceptions import NotFoundError
from app.schemas.vehicle import VehicleListParams

SORT_COLUMNS = {"id": Vehicle.id, "year": Vehicle.year}

class VehicleRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list(self, params: VehicleListParams) -> Sequence[Vehicle]:
        query = (
            self._filtered(params)
            .options(contains_eager(Vehicle.vehicle_model).contains_eager(VehicleModel.brand))
            .order_by(*_sort_clauses(params.sort))
            .offset(params.offset)
            .limit(params.per_page)
        )
        return self._session.scalars(query).all()

    def count(self, params: VehicleListParams) -> int:
        query = self._filtered(params).with_only_columns(func.count(Vehicle.id))
        return self._session.scalar(query) or 0

    def add(self, vehicle: Vehicle) -> Vehicle:
        self._session.add(vehicle)
        self._flush()
        return vehicle

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        query = (
            self._with_model_and_brand()
            .options(contains_eager(Vehicle.vehicle_model).contains_eager(VehicleModel.brand))
            .where(Vehicle.id == vehicle_id)
        )
        return self._session.scalar(query)

    def save(self, vehicle: Vehicle) -> Vehicle:
        self._flush()
        return vehicle

    def delete(self, vehicle: Vehicle) -> None:
        self._session.delete(vehicle)
        self._session.flush()


    def _filtered(self, params: VehicleListParams) -> Select:
        """ The join + every filter. """

        query = self._with_model_and_brand()
        if params.brand_id is not None:
            query = query.where(VehicleModel.brand_id == params.brand_id)
        if params.model_id is not None:
            query = query.where(Vehicle.model_id == params.model_id)
        if params.year_min is not None:
            query = query.where(Vehicle.year >= params.year_min)
        if params.year_max is not None:
            query = query.where(Vehicle.year <= params.year_max)
        if params.has_owner is not None:
            owner = Vehicle.user_id
            query = query.where(owner.is_not(None) if params.has_owner else owner.is_(None))
        return query


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

def _sort_clauses(sort: str) -> tuple:
    # When '-year' it means DESC
    column = SORT_COLUMNS[sort.lstrip("-")]
    return (column.desc() if sort.startswith("-") else column.asc(), Vehicle.id)