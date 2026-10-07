from http import HTTPStatus

from flask import Blueprint

from app.services.rental_service import RentalService
from app.repositories.rental_repository import RentalRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.repositories.user_repository import UserRepository
from app.http.api_response import ApiResponse
from app.http.http_utils import QueryParams, get_json_body

rentals_bp = Blueprint("/rentals", __name__, url_prefix="/rentals")

def _service():
   return RentalService(RentalRepository(), VehicleRepository(), UserRepository())

# List of rentals filtering by status
@rentals_bp.get("")
def list_rentals():
   params = QueryParams(allowed={"status", "user_id", "vehicle_id"})
   status = params.get_str("status")
   user_id = params.get_str("user_id")
   vehicle_id = params.get_str("vehicle_id")
   params.raise_if_errors()
   rentals_list = _service().list_rentals(status=status, user_id=user_id, vehicle_id=vehicle_id)
   return ApiResponse.success("Rentals retrieved successfully.", [rental.to_dict() for rental in rentals_list])

@rentals_bp.post("")
def create_rental_handler():
   rental = _service().create_rental(get_json_body())
   return ApiResponse.success("Rental created successfully.", rental.to_dict(), status=HTTPStatus.CREATED)

@rentals_bp.patch("/<int:rental_id>/complete-rental")
def complete_rental_handler(rental_id):
   rental = _service().complete_rental(rental_id)
   return ApiResponse.success("Rental completed successfully", rental.to_dict())

@rentals_bp.patch("/<int:rental_id>/cancel-rental")
def cancel_rental_handler(rental_id):
   rental = _service().cancel_rental(rental_id)
   return ApiResponse.success("Rental cancelled successfully", rental.to_dict())