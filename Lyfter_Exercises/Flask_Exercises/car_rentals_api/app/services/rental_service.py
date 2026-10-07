from app.models.enums import RentalStatus
from app.http.errors import ValidationError, ConflictError, NotFoundError
from app.models.rental import Rental
from app.models.exceptions import ModelValidationError
from app.utils.validators import clean_int
from app.db import transaction

class RentalService:
    def __init__(self, repository, vehicle_repository, user_repository):
        self._repository = repository
        self._vehicle_repository = vehicle_repository
        self._user_repository = user_repository

    def list_rentals(self, status=None, user_id=None, vehicle_id=None):
        valid_statuses = [s.value for s in RentalStatus]
        if status is not None:
            if status not in valid_statuses:    
                raise ValidationError("Invalid params.", {"status": f"The status must be only: {', '.join(valid_statuses)}"})
        return self._repository.find_all(status, user_id=user_id, vehicle_id=vehicle_id)

    def create_rental(self, data):
        try:
            rental = Rental.create_rental(
                user_id=data.get("user_id"),
                vehicle_id=data.get("vehicle_id")
            )
        except ModelValidationError as error:
            raise ValidationError("Rental data is invalid.", error.errors) from error

        with transaction():
            # Validate if the user exists
            user = self._user_repository.find_by_id(rental.user_id)
            if user is None:
                raise ValidationError(f"Rental data is invalid.", {"user_id": f"User {rental.user_id} does not exist."})

            # Update the status of the vehicle to Rented
            # Since here we are updating the vehicle, the database blocks it in this transaction to avoid other users making updates
            # Atomic check and update, only succeeds if the vehicle exists and is status Available right now 
            if self._vehicle_repository.mark_as_rented(rental.vehicle_id) is None:
                vehicle = self._vehicle_repository.get_by_id(rental.vehicle_id)
                if vehicle is None:
                    raise ValidationError("Rental data is invalid.", {"vehicle_id": f"Vehicle {rental.vehicle_id} does not exist."})
                raise ConflictError(f"Vehicle {rental.vehicle_id} is not available (current status: {vehicle.status})")

            # Create the rental
            rental_id = self._repository.create(rental)
            # Return the created rental
        return self._repository.find_by_id(rental_id)


    def complete_rental(self, rental_id):
        errors = {}
        rental_id = clean_int(rental_id, "rental_id", errors)

        if errors:
            raise ValidationError("Invalid data.", errors)

        with transaction():
            vehicle_id = self._repository.complete_rental(rental_id)
            if vehicle_id is None:
                rental = self._repository.find_by_id(rental_id)
                if rental is None:
                    raise NotFoundError(f"Rental {rental_id} does not exist.")
                raise ConflictError(f"Rental {rental_id} is already in status {rental.status}")
            if self._vehicle_repository.mark_as_available(vehicle_id) is None:
                raise RuntimeError(f"Vehicle {vehicle_id} was not Rented while closing rental {rental_id}.")
            
        return self._repository.find_by_id(rental_id)

    def cancel_rental(self, rental_id):
        with transaction():
            vehicle_id = self._repository.cancel_rental(rental_id)
            if vehicle_id is None:
                rental = self._repository.find_by_id(rental_id)
                if rental is None:
                    raise NotFoundError(f"Rental {rental_id} does not exist.")
                raise ConflictError(f"Rental {rental_id} is already in status {rental.status}")
            if self._vehicle_repository.mark_as_available(vehicle_id) is None:
                raise RuntimeError(f"Vehicle {vehicle_id} was not Rented while cancelling rental {rental_id}")

        return self._repository.find_by_id(rental_id)