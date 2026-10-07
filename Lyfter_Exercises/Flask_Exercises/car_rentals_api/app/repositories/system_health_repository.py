from app.db import get_connection
from psycopg2 import sql

_SELECT_MISSING_TABLES = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = %s
    AND table_name = ANY(%s)
"""
_GET_NUM_ROWS_IN_TABLE = sql.SQL("SELECT COUNT(*) AS num_rows FROM {}")


class SystemHealthRepository:
    REQUIRED_TABLES = ("brands", "rentals", "schema_migrations", "users", "vehicle_models", "vehicles")

    def __init__(self, get_conn=get_connection):
        self._get_conn=get_conn

    def get_missing_tables(self, tables=REQUIRED_TABLES):
        with self._get_conn().cursor() as cursor:
            cursor.execute(_SELECT_MISSING_TABLES, ("lyfter_car_rental", list(tables)))
            existing = {row["table_name"] for row in cursor.fetchall()}
        return set(tables) - existing # Empty means that all tables exist

    def get_num_rows_in_table(self, table_name):
        query = _GET_NUM_ROWS_IN_TABLE.format(sql.Identifier("lyfter_car_rental", table_name))
        with self._get_conn().cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()["num_rows"]