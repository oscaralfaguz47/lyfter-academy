from flask import Blueprint
from app.services.system_health_services import SystemHealthService
from app.repositories.system_health_repository import SystemHealthRepository
from app.http.api_response import ApiResponse

system_health_bp = Blueprint("system-health", __name__, url_prefix="/system-health")

def _service():
    return SystemHealthService(SystemHealthRepository())

@system_health_bp.get("")
def validate_system_health():
    tables_with_rows = _service().get_health_tables()
    return ApiResponse.success("DB OK. System running normally.", tables_with_rows)