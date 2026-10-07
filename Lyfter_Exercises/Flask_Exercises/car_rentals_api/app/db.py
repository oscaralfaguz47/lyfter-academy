from contextlib import contextmanager

import psycopg2
from flask import current_app, g
from psycopg2.extras import RealDictCursor

def get_connection():
    if "db" not in g:
        config = current_app.config
        g.db = psycopg2.connect(
            host=config["DB_HOST"],
            port=config["DB_PORT"],
            dbname=config["DB_NAME"],
            user=config["DB_USER"],
            password=config["DB_PASSWORD"],
            options=f"-c search_path={config['DB_SCHEMA']}",
            cursor_factory=RealDictCursor # The rows come back as dicts: row["name"]
        )
    return g.db

@contextmanager
def transaction():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise

# It runs at the end of every request, even if it failed
def close_connection(error=None):
    conn = g.pop("db", None)
    if conn is not None:
        try:
            conn.rollback() # Discard anything that was not committed explicitly
        finally:
            conn.close() # Always runs, even if rollback fails on a dead connection

def init_app(app):
    app.teardown_appcontext(close_connection)

# MY IMPORTANT NOTES TO REMEMBER:
# The connection is opened automatically in every request and closes as well, if there's an error a rollback is executed
# Here the commit is not executed, it must be implemented in the repository when everything was ok.