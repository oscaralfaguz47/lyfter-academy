from flask import Blueprint, request

from app.services.rental_service import RentalService
from app.repositories.rental_repository import RentalRepository
from app.http.api_response import ApiResponse

rentals_bp = Blueprint("/rentals", __name__, url_prefix="/rentals")

def _service():
   return RentalService(RentalRepository())

# List of rentals filtering by status
@rentals_bp.get("")
def list_rentals():
    status = request.args.get("status")
    rentals_list = _service().list_rentals(status)
    return ApiResponse.success("Rentals retrieved successfully.", [rental.to_dict() for rental in rentals_list])