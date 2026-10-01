from app.db import get_connection
from app.models.vehicle import Vehicle

FIND_ALL = """
    SELECT v.id, 
    v.year, 
    v.status, 
    vm.id AS model_id, 
    vm.name AS model_name,
    b.id AS brand_id,
    b.name AS brand_name 
    FROM vehicles v 
    INNER JOIN vehicle_models vm ON v.model_id = vm.id
    INNER JOIN brands b ON vm.brand_id = b.id
    WHERE (%(model_id)s IS NULL OR v.model_id = %(model_id)s)
    ORDER BY v.id
"""

class VehicleRepository:
    def __init__(self, get_conn=get_connection):
        self._get_conn = get_conn

    def _fetch_one(self, query, params):
        with self._get_conn().cursor() as cursor:
            cursor.execute(query, params)
            cursor.fetchone()

    def fetch_all(self, model_id=None):
        with self._get_conn().cursor() as cursor:
            cursor.execute(FIND_ALL, {"model_id": model_id})
            return [Vehicle.from_row(row) for row in cursor.fetchall()]