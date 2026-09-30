from app.db import get_connection
from app.models.user import User


COLUMNS = "id, full_name, username, email, password, birthdate, status, creation_date"

# Queries
FIND_ALL = f"""
    SELECT {COLUMNS} FROM users
    WHERE (%(username)s::text IS NULL OR username ILIKE '%%' || %(username)s || '%%')
"""

class UserRepository:
    def __init__(self, get_conn=get_connection):
        self._get_conn = get_conn

    def find_all(self, username=None):
        with self._get_conn().cursor() as cursor:
            cursor.execute(FIND_ALL, {"username": username})
            return [User.from_row(row) for row in cursor.fetchall()]