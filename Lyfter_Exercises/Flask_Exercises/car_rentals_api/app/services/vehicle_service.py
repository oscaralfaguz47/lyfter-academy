from app.errors import ValidationError

class VehicleService:
    def __init__(self, repository):
        self._repository = repository

    def list_vehicles(self, model_id=None):
        if model_id is not None:
            try:
                int(model_id)
            except ValueError:
                raise ValidationError("Invalid query params.", {"model_id": "The model_id must be an integer"})
        return self._repository.fetch_all(model_id)