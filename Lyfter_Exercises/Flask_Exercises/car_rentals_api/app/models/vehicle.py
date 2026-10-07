
from app.models.exceptions import ModelValidationError
from app.utils.validators import clean_int
from app.models.vehicle_model import VehicleModel
from app.models.brand import Brand

class Vehicle:
    def __init__(
            self, model_id, year, *, 
            status=None, vehicle_id=None, vehicle_model=None, vehicle_brand=None
        ):
        self.model_id = model_id
        self.year = year
        self.status = status
        self.id = vehicle_id
        self.vehicle_model = vehicle_model
        self.vehicle_brand = vehicle_brand

    @classmethod
    def create_vehicle(cls, *, model_id, year):
        errors = {}

        model_id = clean_int(model_id, "model_id", errors, required=True)
        year = clean_int(year, "year", errors, required=True)

        if errors:
            raise ModelValidationError(errors)

        return cls(
            model_id,
            year
        )

    @classmethod
    def from_row(cls, row):
        vehicle_model = VehicleModel(
            row["model_name"], row["brand_id"],
            model_id=row["model_id"]
        )
        vehicle_brand = Brand(
            row["brand_name"],
            brand_id=row["brand_id"]
        )
        return cls(
            row["model_id"],
            row["year"],
            status=row["status"],
            vehicle_id=row["id"],
            vehicle_model=vehicle_model,
            vehicle_brand=vehicle_brand
        )

    def to_dict(self):
        return {
            "id": self.id,
            "year": self.year,
            "status": self.status,
            "model": self.vehicle_model.to_dict() if self.vehicle_model else self.model_id,
            "brand": self.vehicle_brand.to_dict() if self.vehicle_brand else (self.vehicle_model.brand_id if self.vehicle_model else None)
        }