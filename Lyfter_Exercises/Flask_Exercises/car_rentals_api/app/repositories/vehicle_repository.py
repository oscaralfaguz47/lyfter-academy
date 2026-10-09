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
    AND (%(year)s IS NULL OR v.year = %(year)s)
    AND (%(status)s IS NULL OR v.status = %(status)s)
    ORDER BY v.id
"""
_INSERT = """
    INSERT INTO vehicles (model_id, year, status) 
    VALUES(%(model_id)s, %(year)s, 'Available')
    RETURNING id
"""

_FIND_BY_ID = """
    SELECT
    v.id,
    v.year,
    v.status,
    vm.id AS model_id,
    vm.name AS model_name,
    b.id AS brand_id,
    b.name AS brand_name
    FROM vehicles v
    INNER JOIN vehicle_models vm ON vm.id = v.model_id
    INNER JOIN brands b ON b.id = vm.brand_id
    WHERE v.id = %(id)s
"""

_UPDATE_STATUS = """
    UPDATE vehicles SET status = %(status_for_update)s
    WHERE status = %(current_status)s 
    AND id = %(vehicle_id)s
    RETURNING id
"""

_GET_ALL_FOR_BACKUP = f"""
    SELECT * FROM vehicles ORDER BY id
"""

class VehicleRepository:
    BACKUP_COLUMNS = ("id", "model_id", "year", "status")

    def __init__(self, get_conn=get_connection):
        self._get_conn = get_conn

    def _fetch_one(self, query, params):
        with self._get_conn().cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()
            
    def fetch_all(self, model_id=None, year=None, status=None):
        with self._get_conn().cursor() as cursor:
            cursor.execute(FIND_ALL, {"model_id": model_id, "year": year, "status": status})
            return [Vehicle.from_row(row) for row in cursor.fetchall()]

    def get_by_id(self, vehicle_id):
        row = self._fetch_one(_FIND_BY_ID, {"id": vehicle_id})
        return Vehicle.from_row(row) if row else None

    def create(self, vehicle):
        row = self._fetch_one(_INSERT, self._params(vehicle))
        return row["id"]

    def mark_as_rented(self, vehicle_id):
        row = self._fetch_one(_UPDATE_STATUS, {"vehicle_id": vehicle_id, "status_for_update": "Rented", "current_status": "Available"})
        return row["id"] if row else None

    def mark_as_available(self, vehicle_id):
        row = self._fetch_one(_UPDATE_STATUS, {"vehicle_id": vehicle_id, "status_for_update": "Available", "current_status": "Rented"})
        return row["id"] if row else None 
    
    def update_status(self, vehicle_id, new_status, current_status):
        row = self._fetch_one(_UPDATE_STATUS, {"vehicle_id": vehicle_id, "status_for_update": new_status, "current_status": current_status})
        return row["id"] if row else None

    def get_all_for_backup(self):
        with self._get_conn().cursor() as cursor:
            cursor.execute(_GET_ALL_FOR_BACKUP)
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def _params(vehicle):
        return {
            "model_id": vehicle.model_id,
            "year": vehicle.year
        }