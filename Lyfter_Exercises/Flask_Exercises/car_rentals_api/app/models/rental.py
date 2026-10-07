from app.models.exceptions import ModelValidationError
from app.models.vehicle import Vehicle
from app.models.vehicle_model import VehicleModel
from app.models.brand import Brand
from app.models.user import UserSummary
from app.utils.validators import clean_int

class Rental:
    def __init__(
        self, 
        user_id, 
        vehicle_id,  
        *, 
        status=None,
        rental_id=None, 
        rental_date=None,
        user=None,
        vehicle=None
    ):
        self.user_id = user_id
        self.vehicle_id = vehicle_id
        self.status = status
        self.id = rental_id
        self.rental_date = rental_date
        self.user = user
        self.vehicle = vehicle

    @classmethod
    def create_rental(cls, *, user_id, vehicle_id):
        errors = {}

        user_id = clean_int(user_id, "user_id", errors)
        vehicle_id = clean_int(vehicle_id, "vehicle_id", errors)

        if errors:
            raise ModelValidationError(errors)
        return cls(
            user_id,
            vehicle_id
        )

    @classmethod
    def from_row(cls, row):
        vehicle_model = VehicleModel(
            row["vehicle_model_name"], row["vehicle_brand_id"],
            model_id=row["vehicle_model_id"]
        )
        vehicle_brand = Brand(
            row["vehicle_brand_name"],
            brand_id=row["vehicle_brand_id"]
        )
        vehicle = Vehicle(
            row["vehicle_model_id"], row["vehicle_year"], 
            status=row["vehicle_status"],
            vehicle_id=row["vehicle_id"],
            vehicle_model=vehicle_model,
            vehicle_brand=vehicle_brand
        )
        return cls(
            row["user_id"], row["vehicle_id"], 
            status=row["status"],
            rental_id=row["id"],
            rental_date=row["rental_date"],
            user=UserSummary(row["user_id"], row["user_full_name"]),
            vehicle=vehicle
        )

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user.to_dict() if self.user else {"id": self.user_id},
            "vehicle": self.vehicle.to_dict() if self.vehicle else {"id": self.vehicle_id},
            "rental_date": self.rental_date.isoformat() if self.rental_date else None,
            "status": self.status
        }