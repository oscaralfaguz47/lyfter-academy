from flask import Blueprint, request, url_for

from app.database import get_session

from app.services.vehicle_service import VehicleService
from app.repositories.vehicle_repository import VehicleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.vehicle_model_repository import VehicleModelRepository
from app.schemas.pagination import PaginationParams
from app.schemas.validation import parse
from app.schemas.vehicle import VehicleRead, VehicleCreate, VehicleUpdate, VehicleOwnerAssign
from app.routes.responses import pagination_meta, ok, serialize_many, created, serialize, no_content


vehicles_bp = Blueprint("vehicles", __name__, url_prefix="/api/v1/vehicles")

def _vehicle_service() -> VehicleService:
    session = get_session()
    return VehicleService(session, VehicleRepository(session), UserRepository(session), VehicleModelRepository(session))


@vehicles_bp.get("")
def list_vehicles():
    pagination = parse(PaginationParams, request.args.to_dict(), "Invalid query params")
    vehicles, total = _vehicle_service().list_vehicles(pagination)
    meta = pagination_meta(pagination.page, pagination.per_page, total)
    return ok(serialize_many(VehicleRead, vehicles), meta)

@vehicles_bp.get("/<int:vehicle_id>")
def get_vehicle(vehicle_id: int):
    vehicle = _vehicle_service().get_vehicle(vehicle_id)
    return ok(serialize(VehicleRead, vehicle))

@vehicles_bp.post("")
def create_vehicle():
    data = parse(VehicleCreate, request.get_json())
    vehicle = _vehicle_service().create_vehicle(data)
    return created(serialize(VehicleRead, vehicle), location=url_for("vehicles.get_vehicle", vehicle_id=vehicle.id))

@vehicles_bp.patch("/<int:vehicle_id>")
def update_vehicle(vehicle_id: int):
    data = parse(VehicleUpdate, request.get_json())
    vehicle = _vehicle_service().update_vehicle(vehicle_id, data)
    return ok(serialize(VehicleRead, vehicle))

@vehicles_bp.delete("/<int:vehicle_id>")
def delete_vehicle(vehicle_id: int):
    _vehicle_service().delete_vehicle(vehicle_id)
    return no_content()

@vehicles_bp.put("/<int:vehicle_id>/owner")
def assign_owner(vehicle_id: int):
    data = parse(VehicleOwnerAssign, request.get_json())
    vehicle = _vehicle_service().assign_owner(vehicle_id, data.user_id)
    return ok(serialize(VehicleRead, vehicle))

@vehicles_bp.delete("/<int:vehicle_id>/owner")
def remove_owner(vehicle_id: int):
    vehicle = _vehicle_service().remove_owner(vehicle_id)
    return ok(serialize(VehicleRead, vehicle))