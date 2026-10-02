from app.models.enums import RentalStatus
from app.http.errors import ValidationError

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
        if not isinstance(data, dict):
            raise ValidationError("Model must be a valid JSON object.")