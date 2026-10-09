from app.http.errors import ValidationError, NotFoundError, ConflictError
from app.models.vehicle import Vehicle
from app.models.enums import VehicleStatus
from app.models.exceptions import ModelValidationError
from app.utils.validators import clean_str
from app.db import transaction

# Manual status changes allowed through the API: {new_status: required_current_status}
# Rented is excluded on purpose, only RentalService moves a vehicle in or out of Rented
STATUS_TRANSITIONS = {
    VehicleStatus.MAINTENANCE.value: VehicleStatus.AVAILABLE.value,
    VehicleStatus.AVAILABLE.value: VehicleStatus.MAINTENANCE.value,
}

class VehicleService:
    def __init__(self, repository, vehicle_model_repository):
        self._repository = repository
        self._vehicle_model_repository = vehicle_model_repository

    def list_vehicles(self, model_id=None, year=None, status=None):
        valid_statuses = [s.value for s in VehicleStatus]
        if status is not None and status not in valid_statuses:
            raise ValidationError("Invalid params.", {"status": f"The status must be only: {', '.join(valid_statuses)}"})
        return self._repository.fetch_all(model_id=model_id, year=year, status=status)

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
            raise NotFoundError(f"Model {vehicle_to_create.model_id} does not exist.")

        with transaction():
            vehicle_id = self._repository.create(vehicle_to_create)

        return self._repository.get_by_id(vehicle_id)

    def update_status(self, vehicle_id, data):
        errors = {}
        status = clean_str(data.get("status"), "status", errors)
        if status is not None and status not in STATUS_TRANSITIONS:
            errors["status"] = f"Must be only: {', '.join(STATUS_TRANSITIONS)}"
        if errors:
            raise ValidationError("Vehicle data is invalid.", errors)

        with transaction():
            # Atomic check and update, only succeeds if the vehicle exists and is in the required status right now
            if self._repository.update_status(vehicle_id, status, STATUS_TRANSITIONS[status]) is None:
                vehicle = self._repository.get_by_id(vehicle_id)
                if vehicle is None:
                    raise NotFoundError(f"Vehicle {vehicle_id} does not exist.")
                raise ConflictError(f"Vehicle {vehicle_id} cannot change from {vehicle.status} to {status}.")

        return self._repository.get_by_id(vehicle_id)