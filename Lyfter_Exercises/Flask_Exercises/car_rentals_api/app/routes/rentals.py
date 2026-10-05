from flask import Blueprint

from app.services.rental_service import RentalService
from app.repositories.rental_repository import RentalRepository
from app.http.api_response import ApiResponse
from app.http.http_utils import QueryParams, get_json_body

rentals_bp = Blueprint("/rentals", __name__, url_prefix="/rentals")

def _service():
   return RentalService(RentalRepository())

# List of rentals filtering by status
@rentals_bp.get("")
def list_rentals():
   params = QueryParams(allowed={"status"})
   status = params.get_str("status")
   params.raise_if_errors()
   rentals_list = _service().list_rentals(status)
   return ApiResponse.success("Rentals retrieved successfully.", [rental.to_dict() for rental in rentals_list])

@rentals_bp.post("")
def create_rental_handler():
   rental = _service().create_rental(get_json_body())
   return ApiResponse.success("Rental created successfully.", rental.to_dict())

@rentals_bp.patch("/<int:rental_id>/status")
def update_status_handler(rental_id):
   rental = _service().update_status(rental_id, get_json_body())
   return ApiResponse.success("Status updated successfully.", rental.to_dict())

@rentals_bp.patch("/<int:rental_id>/complete-rental")
def complete_rental_handler(rental_id):
   rental = _service().update_status(rental_id, {"status": "Completed"})
   return ApiResponse.success("Rental completed successfully", rental.to_dict())
