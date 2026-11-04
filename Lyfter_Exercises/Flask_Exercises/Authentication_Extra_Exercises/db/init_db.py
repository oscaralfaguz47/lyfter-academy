from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, inspect

import app.models  # Registers every model in Base.metadata, DO NOT REMOVE
from app.config import get_config
from app.database import Base, create_db_engine

ALEMBIC_INI = "alembic.ini"


def find_missing_tables(engine: Engine) -> list[str]:
    inspector = inspect(engine)
    expected = [table.name for table in Base.metadata.sorted_tables]
    return [name for name in expected if not inspector.has_table(name)]


def create_tables(engine: Engine, names: list[str]) -> None:
    tables = [Base.metadata.tables[name] for name in names]
    Base.metadata.create_all(engine, tables=tables)


def mark_migrations_as_applied() -> None:
    command.stamp(Config(ALEMBIC_INI), "head")


def main() -> None:
    config = get_config()
    engine = create_db_engine(config.DATABASE_URL, config.DB_SCHEMA)
    try:
        missing = find_missing_tables(engine)
        for table in Base.metadata.sorted_tables:
            status = "MISSING" if table.name in missing else "ok"
            print(f"{table.name:<16} {status}")

        if not missing:
            print("All tables exist, nothing to create.")
            return

        create_tables(engine, missing)
        print(f"Created: {', '.join(missing)}")
        mark_migrations_as_applied()
        print("Alembic stamped at head.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()