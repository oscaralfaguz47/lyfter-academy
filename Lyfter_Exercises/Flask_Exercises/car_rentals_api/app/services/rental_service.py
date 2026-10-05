from app.models.enums import RentalStatus
from app.http.errors import ValidationError
from app.models.rental import Rental
from app.models.exceptions import ModelValidationError
from app.utils.validators import clean_str, clean_int

class RentalService:
    def __init__(self, repository):
        self._repository = repository

    def list_rentals(self, status=None):
        valid_statuses = [s.value for s in RentalStatus]
        if status is not None:
            if status not in valid_statuses:    
                raise ValidationError("Invalid params.", {"status": f"The status must by only: {', '.join(valid_statuses)}"})
        return self._repository.find_all(status)

    def create_rental(self, data):
        try:
            rental = Rental.create_rental(
                user_id=data.get("user_id"),
                vehicle_id=data.get("vehicle_id"),
                status=data.get("status") 
            )
        except ModelValidationError as error:
            raise ValidationError("Rental data is invalid.", error.errors) from error
        rental_id = self._repository.create(rental)
        return self._repository.find_by_id(rental_id)

    def update_status(self, rental_id, data):
        errors = {}
        rental_id = clean_int(rental_id, "rental_id", errors)
        status = clean_str(data["status"], "status", errors)

        valid_statuses = [s.value for s in RentalStatus]

        if status not in valid_statuses:
            errors["status"] = f"The status must be only: {', '.join(valid_statuses)}"

        if errors:
            raise ValidationError("Invalid data", errors)

        return self._repository.update_status(rental_id, status)

