from flask import Blueprint, request

from app.database import get_session

from app.services.vehicle_service import VehicleService
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.pagination import PaginationParams
from app.schemas.validation import parse
from app.schemas.vehicle import vehicleRead
from app.routes.responses import pagination_meta, ok, serialize_many


vehicles_bp = Blueprint("vehicles", __name__, url_prefix="/api/v1/vehicles")

def _vehicle_service() -> VehicleService:
    session = get_session()
    return VehicleService(session, VehicleRepository(session))


@vehicles_bp.get("")
def list_vehicles():
    pagination = parse(PaginationParams, request.args.to_dict(), "Invalid query params")
    vehicles, total = _vehicle_service().list_vehicles(pagination)
    meta = pagination_meta(pagination.page, pagination.per_page, total)
    return ok(serialize_many(vehicleRead, vehicles), meta)

