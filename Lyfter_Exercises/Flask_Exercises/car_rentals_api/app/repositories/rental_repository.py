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
    ORDER BY r.id
"""

class RentalRepository:
    def __init__(self, get_conn=get_connection):
        self._get_conn = get_conn

    def _fetch_one(self, query, params):
        with self._get_conn().cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def find_all(self, status=None):
        with self._get_conn().cursor() as cursor:
            cursor.execute(FIND_ALL, {"status":status})
            return [Rental.from_row(row) for row in cursor.fetchall()]

