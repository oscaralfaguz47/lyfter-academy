from http import HTTPStatus

from flask import Blueprint

from app.repositories.backup_repository import BackupRepository
from app.repositories.user_repository import UserRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.repositories.rental_repository import RentalRepository
from app.repositories.vehicle_model_repository import VehicleModelRepository
from app.repositories.brand_repository import BrandRepository
from app.services.backup_service import BackupService

from app.http.api_response import ApiResponse

backup_bp = Blueprint("backup", __name__, url_prefix="/backup")

def _service():
    return BackupService(
        BackupRepository(), 
        UserRepository(), 
        VehicleRepository(), 
        RentalRepository(), 
        VehicleModelRepository(), 
        BrandRepository()
    )

@backup_bp.post("")
def create_backup():
    backed_up_files = _service().backup_all_db_data()
    return ApiResponse.success("Backup created successfully", backed_up_files, status=HTTPStatus.CREATED)
