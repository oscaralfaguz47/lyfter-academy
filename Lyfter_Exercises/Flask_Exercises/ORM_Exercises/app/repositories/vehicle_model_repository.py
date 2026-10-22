
from sqlalchemy.orm import Session

from app.models.vehicle_model import VehicleModel

class VehicleModelRepository:
    def __init__(self, session: Session) -> None:
        self._session = session


    def get_by_id(self, model_id: int) -> VehicleModel | None:
        return self._session.get(VehicleModel, model_id)