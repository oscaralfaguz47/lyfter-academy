from app.db import get_connection
from app.models.rental import Rental

FIND_ALL = """
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
    ORDER BY r.id
"""

INSERT = """
    INSERT INTO rentals (user_id, vehicle_id, status)
    VALUES(%(user_id)s, %(vehicle_id)s, %(status)s)
    RETURNING id
"""
FIND_BY_ID = """
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
UPDATE_STATUS = """
    UPDATE rentals SET status = %(status)s
    WHERE id = %(rental_id)s
    RETURNING id
"""

GET_ALL_FOR_BACKUP = """
    SELECT * FROM rentals
"""

class RentalRepository:
    def __init__(self, get_conn=get_connection):
        self._get_conn = get_conn

    def _fetch_one(self, query, params):
        with self._get_conn().cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def find_all(self, status=None, user_id=None):
        with self._get_conn().cursor() as cursor:
            cursor.execute(FIND_ALL, {"status":status, "user_id": user_id})
            return [Rental.from_row(row) for row in cursor.fetchall()]

    def find_by_id(self, rental_id):
        row = self._fetch_one(FIND_BY_ID, {"rental_id": rental_id})
        return Rental.from_row(row) if row else None

    def create(self, rental):
        conn = self._get_conn()
        row = self._fetch_one(INSERT, self._params(rental))
        conn.commit()
        return row["id"]

    def update_status(self, rental_id, status):
        conn = self._get_conn()
        row = self._fetch_one(UPDATE_STATUS, {"rental_id": rental_id, "status": status})
        conn.commit()
        return self.find_by_id(row["id"])

    def get_active_rentals_by_user_id(self, user_id):
        with self._get_conn().cursor() as cursor:
            cursor.execute(FIND_ALL, {"user_id": user_id, "status":"Active"})
            return [Rental.from_row(row) for row in cursor.fetchall()]

    def get_all_for_backup(self):
        with self._get_conn().cursor() as cursor:
            cursor.execute(GET_ALL_FOR_BACKUP)
            return [Rental.from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def _params(rental):
        return {
            "user_id": rental.user_id,
            "vehicle_id": rental.vehicle_id,
            "status": rental.status
        }

