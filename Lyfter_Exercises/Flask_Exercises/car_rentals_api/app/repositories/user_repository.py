from app.db import get_connection
from app.models.user import User
from psycopg2 import errors as pg_errors
from app.repositories.exceptions import DuplicateRecordError


COLUMNS = "id, full_name, username, email, birthdate, status, creation_date"

# Queries
FIND_ALL = f"""
    SELECT {COLUMNS} FROM users
    WHERE (%(username)s::text IS NULL OR username ILIKE '%%' || %(username)s || '%%')
    AND (%(full_name)s IS NULL OR full_name = %(full_name)s)
    AND (%(email)s::text IS NULL OR email ILIKE '%%' || %(email)s || '%%')
    AND (%(birthdate)s IS NULL OR birthdate = %(birthdate)s)
    AND (%(status)s IS NULL OR status = %(status)s)
    ORDER BY id
"""
INSERT = f"""
    INSERT INTO users (full_name, username, email, password, birthdate, status) 
    VALUES(%(full_name)s, %(username)s, %(email)s, %(password)s, %(birthdate)s, %(status)s)
    RETURNING {COLUMNS}
"""
UPDATE_STATUS = f"""
    UPDATE users SET status = %(status)s WHERE id = %(id)s RETURNING {COLUMNS}
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

    def create(self, user):
        conn = self._get_conn()
        try:
            row = self._fetch_one(INSERT, self._params(user))
        except pg_errors.UniqueViolation as error:
            raise DuplicateRecordError(str(error)) from error
        conn.commit()
        return User.from_row(row)

    def update_status(self, user_id, status):
        row = self._fetch_one(UPDATE_STATUS, {"id": user_id, "status": status})
        self._get_conn().commit()
        return User.from_row(row) if row else None # Return the updated user or None if it doesn't exist
        

    @staticmethod
    def _params(user):
        return {
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "birthdate": user.birthdate,
            "status": user.status
        }