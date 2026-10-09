from app.db import get_connection
from app.models.brand import Brand


_GET_ALL_FOR_BACKUP = f"""
    SELECT * FROM brands ORDER BY id
"""

class BrandRepository:
    BACKUP_COLUMNS = ("id", "name")
    def __init__(self, get_conn=get_connection):
        self._get_conn=get_conn

    def get_all_for_backup(self):
        with self._get_conn().cursor() as cursor:
            cursor.execute(_GET_ALL_FOR_BACKUP)
            return [dict(row) for row in cursor.fetchall()]
