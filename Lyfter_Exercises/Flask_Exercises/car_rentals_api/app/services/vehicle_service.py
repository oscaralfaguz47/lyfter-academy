from app.http.errors import ValidationError
from app.models.vehicle import Vehicle
from app.models.exceptions import ModelValidationError
from app.models.enums import VehicleStatus

class VehicleService:
    def __init__(self, repository):
        self._repository = repository

    def list_vehicles(self, model_id=None):
        model_id_parameter = model_id
        if model_id is not None:
            try:
                model_id_parameter = int(model_id_parameter)
            except ValueError:
                raise ValidationError("Invalid query params.", {"model_id": "The model_id must be an integer"})
        return self._repository.fetch_all(model_id_parameter)

    def create_vehicle(self, data):
        if not isinstance(data, dict):
            raise ValidationError("Body must be a valid JSON.")
        try:
            vehicle_to_create = Vehicle.create_vehicle(
                model_id=data.get("model_id"),
                year=data.get("year"),
                status=data.get("status")
                )
        except ModelValidationError as error:
            raise ValidationError("Vehicle data is invalid.", error.errors) from error
        vehicle_id = self._repository.create(vehicle_to_create)
        return self._repository.get_by_id(vehicle_id)

    def update_status(self, vehicle_id, json_data):
        valid_statuses = [s.value for s in VehicleStatus]
        status = json_data["status"]
        if not isinstance(json_data, dict):
            raise ValidationError("Body must be a JSON object")
        if not isinstance(status, str) or not status.strip():
            raise ValidationError("User data is invalid.", {"status": "This field is required."})
        elif status not in valid_statuses:
            raise ValidationError("Vehicle data is invalid.", {"status": f"Must be only: {', '.join(valid_statuses)}"})
        vehicle_id = self._repository.update_status(vehicle_id, status)
        return self._repository.get_by_id(vehicle_id)