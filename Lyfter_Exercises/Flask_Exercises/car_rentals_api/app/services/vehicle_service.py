from app.http.errors import ValidationError, NotFoundError
from app.models.vehicle import Vehicle
from app.models.exceptions import ModelValidationError
from app.db import transaction

class VehicleService:
    def __init__(self, repository, vehicle_model_repository):
        self._repository = repository
        self._vehicle_model_repository = vehicle_model_repository

    def list_vehicles(self, model_id=None):
        model_id_parameter = model_id
        if model_id is not None:
            try:
                model_id_parameter = int(model_id_parameter)
            except ValueError:
                raise ValidationError("Invalid query params.", {"model_id": "The model_id must be an integer"})
        return self._repository.fetch_all(model_id_parameter)

    def create_vehicle(self, data):
        try:
            vehicle_to_create = Vehicle.create_vehicle(
                model_id=data.get("model_id"),
                year=data.get("year")
                )
        except ModelValidationError as error:
            raise ValidationError("Vehicle data is invalid.", error.errors) from error
        model = self._vehicle_model_repository.find_by_id(vehicle_to_create.model_id)
        if model is None:
            NotFoundError(f"Model {vehicle_to_create.model_id} does not exist.")

        with transaction():
            vehicle_id = self._repository.create(vehicle_to_create)
        
        return self._repository.get_by_id(vehicle_id)
