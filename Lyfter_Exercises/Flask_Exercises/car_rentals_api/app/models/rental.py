from app.models.enums import RentalStatus
from app.models.exceptions import ModelValidationError
from app.models.vehicle import Vehicle
from app.models.user import UserSummary
from app.utils.validators import clean_int, clean_str

class Rental:
    def __init__(
        self, 
        user_id, 
        vehicle_id, 
        status, 
        *, 
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
    def create_rental(cls, *, user_id, vehicle_id, status):
        errors = {}
        valid_statuses = [s.value for s in RentalStatus]

        user_id = clean_int(user_id, "user_id", errors)
        vehicle_id = clean_int(vehicle_id, "vehicle_id", errors)
        status = clean_str(status, "status", errors)

        if status not in valid_statuses:
            errors["status"] = f"The status must be only: {', '.join(valid_statuses)}"

        if errors:
            raise ModelValidationError(errors)
        return cls(
            user_id,
            vehicle_id,
            status.strip()
        )

    @classmethod
    def from_row(cls, row):
        vehicle = Vehicle(
            row["vehicle_model_id"], row["vehicle_year"], row["vehicle_status"],
            vehicle_id=row["vehicle_id"],
            model_name=row["vehicle_model_name"],
            brand_id=row["vehicle_brand_id"],
            brand_name=row["vehicle_brand_name"]
        )
        return cls(
            row["user_id"], row["vehicle_id"], row["status"],
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