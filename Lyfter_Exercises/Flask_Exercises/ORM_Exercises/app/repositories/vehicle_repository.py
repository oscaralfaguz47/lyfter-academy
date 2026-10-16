from sqlalchemy.orm import Session
from sqlalchemy import select, func

from collections.abc import Sequence

from app.models.vehicle import Vehicle

class VehicleRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list(self, offset: int, limit: int) -> Sequence["Vehicle"]:
        query = select(Vehicle).order_by(Vehicle.id).offset(offset).limit(limit)
        return self._session.scalars(query).all()

    def count(self) -> int:
        return self._session.scalar(select(func.count()).select_from(Vehicle)) or 0