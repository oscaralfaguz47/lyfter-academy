from app.db import get_connection
from app.models.user import User
from psycopg2 import errors as pg_errors
from app.repositories.exceptions import DuplicateRecordError
from app.models.enums import RentalStatus


COLUMNS = "id, full_name, username, email, birthdate, status, creation_date, has_pending_payments"

# Queries
FIND_ALL = f"""
    SELECT {COLUMNS} FROM users
    WHERE (%(username)s::text IS NULL OR username ILIKE '%%' || %(username)s || '%%')
    AND (%(full_name)s::text IS NULL OR full_name ILIKE '%%' || %(full_name)s || '%%')
    AND (%(email)s::text IS NULL OR email ILIKE '%%' || %(email)s || '%%')
    AND (%(birthdate)s IS NULL OR birthdate = %(birthdate)s)
    AND (%(status)s IS NULL OR status = %(status)s)
    ORDER BY id
"""
INSERT = f"""
    INSERT INTO users (full_name, username, email, password, birthdate) 
    VALUES(%(full_name)s, %(username)s, %(email)s, %(password)s, %(birthdate)s)
    RETURNING {COLUMNS}
"""
UPDATE_STATUS = f"""
    UPDATE users SET status = %(status)s WHERE id = %(id)s RETURNING {COLUMNS}
"""
FLAG_USER_AS_NON_PAYING = """
    UPDATE users u SET has_pending_payments = EXISTS (
    SELECT 1 FROM rentals r 
    WHERE r.user_id = u.id
    AND r.status = %(active_status)s
)
WHERE u.id = %(user_id)s 
RETURNING u.id, u.has_pending_payments
"""
FIND_BY_ID = f"""
    SELECT {COLUMNS} FROM users WHERE id = %(user_id)s
"""

class UserRepository:
    def __init__(self, get_conn=get_connection):
        self._get_conn = get_conn

    def _fetch_one(self, query, params):
        with self._get_conn().cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def find_all(self, username=None, full_name=None, email=None, birthdate=None, status=None):
        with self._get_conn().cursor() as cursor:
            cursor.execute(
                FIND_ALL, {
                    "username": username,
                    "full_name": full_name,
                    "email": email,
                    "birthdate": birthdate,
                    "status": status
                }
            )
            return [User.from_row(row) for row in cursor.fetchall()]

    def find_by_id(self, user_id):
        row = self._fetch_one(FIND_BY_ID, {"user_id": user_id})
        return User.from_row(row) if row else None

    def create(self, user):
        try:
            row = self._fetch_one(INSERT, self._params(user))
        except pg_errors.UniqueViolation as error:
            raise DuplicateRecordError(str(error)) from error
        return User.from_row(row)

    def update_status(self, user_id, status):
        row = self._fetch_one(UPDATE_STATUS, {"id": user_id, "status": status})
        return User.from_row(row) if row else None # Return the updated user or None if it doesn't exist

    def flag_user_as_non_paying(self, user_id):
        row = self._fetch_one(FLAG_USER_AS_NON_PAYING, {"user_id": user_id, "active_status": RentalStatus.ACTIVE.value})
        return row if row else None
        

    @staticmethod
    def _params(user):
        return {
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "birthdate": user.birthdate
        }