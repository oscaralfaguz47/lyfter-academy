from flask import Blueprint, request
from app.services.vehicle_service import VehicleService
from app.repositories.vehicle_repository import VehicleRepository
from app.http.api_response import ApiResponse

vehicles_bp = Blueprint("vehicles", __name__, url_prefix="/vehicles")

def _service(): 
    return VehicleService(VehicleRepository())

# List of vehicles filtering by model_id
@vehicles_bp.get("")
def list_vehicles_handler():
    model_id = request.args.get("model_id")
    vehicles_list = _service().list_vehicles(model_id)
    return ApiResponse.success(
            "Vehicles retrieved successfully", 
            [vehicle.to_dict() for vehicle in vehicles_list]
        )

@vehicles_bp.post("")
def create_vehicle_handler():
    vehicle = _service().create_vehicle(request.get_json(silent=True))
    return ApiResponse.success("Vehicle created successfully.", vehicle.to_dict())

@vehicles_bp.patch("/<int:vehicle_id>/status")
def update_status(vehicle_id):
    vehicle = _service().update_status(vehicle_id, request.json)
    return ApiResponse.success("Status updated successfully.", vehicle.to_dict())