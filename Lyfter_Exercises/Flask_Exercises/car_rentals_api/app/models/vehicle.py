
from app.models.enums import VehicleStatus
from app.models.exceptions import ModelValidationError
from app.utils.validators import clean_int, clean_str

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

    @classmethod
    def create_vehicle(cls, *, model_id, year, status):
        valid_statuses = [s.value for s in VehicleStatus]
        errors = {}

        model_id = clean_int(model_id, "model_id", errors, required=True)
        year = clean_int(year, "year", errors, required=True)
        status = clean_str(status, "status", errors, required=True)
        
        if status.strip() not in valid_statuses:
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