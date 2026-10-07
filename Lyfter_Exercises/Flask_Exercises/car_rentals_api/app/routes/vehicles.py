from http import HTTPStatus

from flask import Blueprint
from app.services.vehicle_service import VehicleService
from app.repositories.vehicle_repository import VehicleRepository
from app.repositories.vehicle_model_repository import VehicleModelRepository
from app.http.api_response import ApiResponse
from app.http.http_utils import get_json_body, QueryParams

vehicles_bp = Blueprint("vehicles", __name__, url_prefix="/vehicles")

def _service(): 
    return VehicleService(VehicleRepository(), VehicleModelRepository())

# List of vehicles filtering by model_id
@vehicles_bp.get("")
def list_vehicles_handler():
    params = QueryParams(allowed={"model_id"})
    model_id = params.get_int("model_id")
    params.raise_if_errors()
    vehicles_list = _service().list_vehicles(model_id)
    return ApiResponse.success(
            "Vehicles retrieved successfully", 
            [vehicle.to_dict() for vehicle in vehicles_list]
        )

@vehicles_bp.post("")
def create_vehicle_handler():
    vehicle = _service().create_vehicle(get_json_body())
    return ApiResponse.success("Vehicle created successfully.", vehicle.to_dict(), status=HTTPStatus.CREATED)

