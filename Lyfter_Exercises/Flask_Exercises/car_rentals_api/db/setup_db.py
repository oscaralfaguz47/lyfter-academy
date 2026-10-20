import os
import sys
from pathlib import Path
import argparse

from dotenv import load_dotenv
from psycopg2 import sql
import psycopg2

from seeds.fake_data import seed_fake_data


# Paths and configuration
DB_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DB_DIR.parent
MIGRATIONS_DIR = DB_DIR / "migrations"
SEEDS_DIR = DB_DIR / "seeds"

load_dotenv(PROJECT_ROOT / ".env")

def _required(name):
    value = os.environ.get(name)
    if not value:
        sys.exit(f"Missing required environment variable: {name}, check your .env file")
    return value

DB_SCHEMA = _required("DB_SCHEMA")
CONNECTION_PARAMS = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5432"),
    "dbname": _required("DB_NAME"),
    "user": _required("DB_USER"),
    "password": os.environ.get("DB_PASSWORD")
}

# Create the schema and make it the default for this connection
def prepare_schema(conn):
    schema = sql.Identifier(DB_SCHEMA)
    with conn.cursor() as cursor:
        cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(schema))
        cursor.execute(sql.SQL("SET search_path TO {}").format(schema))
    conn.commit() 
    print(f"Schema '{DB_SCHEMA}' created.")

# Apply the migrations 
def get_applied_migrations(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                filename TEXT PRIMARY KEY,
                applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
        """)
        cursor.execute("SELECT filename FROM schema_migrations")
        applied = {row[0] for row in cursor.fetchall()}
    conn.commit()
    return applied

def run_migrations(conn):
    applied = get_applied_migrations(conn)
    pending = [path for path in sorted(MIGRATIONS_DIR.glob("*.sql")) if path.name not in applied]

    if not pending:
        print("No pending migrations to apply.")
        return

    for path in pending:
        with conn.cursor() as cursor:
            cursor.execute(path.read_text(encoding="utf-8"))
            cursor.execute(
                "INSERT INTO schema_migrations (filename) VALUES (%s)", (path.name,)
            )
        conn.commit()
        print(f"Applied migration {path.name}")

# Seeds, idempotent files
def run_seeds(conn):
    for path in sorted(SEEDS_DIR.glob("*.sql")):
        with conn.cursor() as cursor:
            cursor.execute(path.read_text(encoding="utf-8"))
        conn.commit()
        print(f"Ran seed {path.name}")

# Entry point, one connection and three steps
def main():
    parser = argparse.ArgumentParser(description="Set up the database.")
    parser.add_argument("--fake", action="store_true", help="Also insert fake data.")
    args = parser.parse_args()

    conn = psycopg2.connect(**CONNECTION_PARAMS)
    try:
        prepare_schema(conn)
        run_migrations(conn)
        run_seeds(conn)
        if args.fake:
            summary = seed_fake_data(conn)
            print(f"Inserted fake data: {summary}")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    print("Database setup completed.")

if __name__ == "__main__":
    main()