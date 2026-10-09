from app.db import get_connection
from app.models.vehicle_model import VehicleModel

_FIND_BY_ID = """
    SELECT 
    vm.id,
    vm.name,
    b.id AS brand_id,
    b.name AS brand_name
    FROM vehicle_models vm
    INNER JOIN brands b ON b.id = vm.brand_id
    WHERE vm.id = %(model_id)s
"""
_GET_ALL_FOR_BACKUP = f"""
    SELECT * FROM vehicle_models ORDER BY id
"""

class VehicleModelRepository:
    BACKUP_COLUMNS = ("id", "name", "brand_id")

    def __init__(self, get_conn=get_connection):
        self._get_conn = get_conn

    def _fetch_one(self, query, params):
        with self._get_conn().cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def find_by_id(self, model_id):
        row = self._fetch_one(_FIND_BY_ID, {"model_id": model_id})
        return VehicleModel.from_row(row) if row else None

    def get_all_for_backup(self):
        with self._get_conn().cursor() as cursor:
            cursor.execute(_GET_ALL_FOR_BACKUP)
            return [dict(row) for row in cursor.fetchall()]