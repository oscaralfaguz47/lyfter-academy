
from app.models.enums import VehicleStatus
from app.models.exceptions import ModelValidationError

class Vehicle:
    def __init__(
            self, model_id, year, status, *, 
            vehicle_id=None, model_name=None, brand_id=None, brand_name=None
        ):
        self.model_id = model_id
        self.year = year
        self.status = status
        self.id = vehicle_id
        self.model_id = model_id
        self.model_name = model_name
        self.brand_id = brand_id
        self.brand_name = brand_name

    def create_vehicle(cls, *, model_id, year, status):
        valid_statuses = [s.value for s in VehicleStatus]
        errors = {}
        if not isinstance(model_id, int):
            errors["model_id"] = "The model_id should be an integer."
        elif not model_id:
            errors["model_id"] = "The model_id is required."
        if not isinstance(year, int):
            errors["year"] = "The year must be an integer."
        elif not year:
            errors["year"] = "The year is required."
        if not isinstance(status, str) or not status.strip():
            errors["status"] = "The status is required."
        elif status.strip() not in valid_statuses:
            errors["status"] = f"Valid status only: {', '.join(valid_statuses)}"

        if errors:
            raise ModelValidationError(errors)

        return cls(
            model_id,
            year,
            status.strip()
        )

    @classmethod
    def from_row(cls, row):
        return cls(
            row["model_id"],
            row["year"],
            row["status"],
            vehicle_id=row["id"],
            model_name=row["model_name"],
            brand_id=row["brand_id"],
            brand_name=row["brand_name"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "year": self.year,
            "status": self.status,
            "model": {
                "id": self.model_id,
                "name": self.model_name
            },
            "brand": {
                "id": self.brand_id,
                "name": self.brand_name
            }
        }