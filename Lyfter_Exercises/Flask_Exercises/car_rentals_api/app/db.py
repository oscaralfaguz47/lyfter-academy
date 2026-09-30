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

# It runs at the end of every request, even if it failed
def close_connection(error=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.rollback() # Discard anything that was not committed explicitly
        conn.close()

def init_app(app):
    app.teardown_appcontext(close_connection)