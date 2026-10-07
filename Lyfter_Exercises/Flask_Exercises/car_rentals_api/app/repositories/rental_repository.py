from app.db import get_connection
from app.models.rental import Rental
from app.models.enums import RentalStatus

_FIND_ALL = """
    SELECT 
    r.id,
    r.rental_date,
    r.status,
    u.id AS user_id,
    u.full_name AS user_full_name,
    v.id AS vehicle_id,
    v.year AS vehicle_year,
    v.status AS vehicle_status,
    vm.id AS vehicle_model_id,
    vm.name AS vehicle_model_name,
    b.id AS vehicle_brand_id,
    b.name AS vehicle_brand_name
    FROM rentals r
    INNER JOIN users u ON u.id = r.user_id
    INNER JOIN vehicles v ON v.id = r.vehicle_id
    INNER JOIN vehicle_models vm ON vm.id = v.model_id
    INNER JOIN brands b ON b.id = vm.brand_id
    WHERE (%(status)s IS NULL OR r.status = %(status)s)
    AND (%(user_id)s IS NULL OR  r.user_id = %(user_id)s)
    AND (%(vehicle_id)s IS NULL OR  r.vehicle_id = %(vehicle_id)s)
    ORDER BY r.id
"""

_INSERT = """
    INSERT INTO rentals (user_id, vehicle_id, status)
    VALUES(%(user_id)s, %(vehicle_id)s, %(status)s)
    RETURNING id
"""
_FIND_BY_ID = """
    SELECT
    r.id,
    r.rental_date,
    r.status,
    u.id AS user_id,
    u.full_name AS user_full_name,
    v.id AS vehicle_id,
    v.year AS vehicle_year,
    v.status AS vehicle_status,
    vm.id AS vehicle_model_id,
    vm.name AS vehicle_model_name,
    b.id AS vehicle_brand_id,
    b.name AS vehicle_brand_name
    FROM rentals r
    INNER JOIN users u ON u.id = r.user_id
    INNER JOIN vehicles v ON v.id = r.vehicle_id
    INNER JOIN vehicle_models vm ON vm.id = v.model_id
    INNER JOIN brands b ON b.id = vm.brand_id
    WHERE r.id = %(rental_id)s
    ORDER BY r.rental_date
"""
_UPDATE_RENTAL_STATUS = """
    UPDATE rentals SET status = %(status)s
    WHERE id = %(rental_id)s
    AND status = 'Active'
    RETURNING id, vehicle_id
"""

_GET_ALL_FOR_BACKUP = f"""
    SELECT * FROM rentals ORDER BY id
"""

class RentalRepository:
    BACKUP_COLUMNS = ("id", "user_id", "vehicle_id", "rental_date", "status")

    def __init__(self, get_conn=get_connection):
        self._get_conn = get_conn

    def _fetch_one(self, query, params):
        with self._get_conn().cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def find_all(self, status=None, user_id=None, vehicle_id=None):
        with self._get_conn().cursor() as cursor:
            cursor.execute(_FIND_ALL, {"status":status, "user_id": user_id, "vehicle_id": vehicle_id})
            return [Rental.from_row(row) for row in cursor.fetchall()]

    def find_by_id(self, rental_id):
        row = self._fetch_one(_FIND_BY_ID, {"rental_id": rental_id})
        return Rental.from_row(row) if row else None

    def create(self, rental):
        row = self._fetch_one(_INSERT, self._params(rental))
        return row["id"]

    def complete_rental(self, rental_id):
        row = self._fetch_one(_UPDATE_RENTAL_STATUS, {"rental_id": rental_id, "status":"Completed"})
        return row["vehicle_id"] if row else None

    def cancel_rental(self, rental_id):
        row = self._fetch_one(_UPDATE_RENTAL_STATUS, {"rental_id": rental_id, "status": "Cancelled"})
        return row["vehicle_id"]if row else None

    def get_all_for_backup(self):
        with self._get_conn().cursor() as cursor:
            cursor.execute(_GET_ALL_FOR_BACKUP)
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def _params(rental):
        return {
            "user_id": rental.user_id,
            "vehicle_id": rental.vehicle_id,
            "status": RentalStatus.ACTIVE.value
        }

