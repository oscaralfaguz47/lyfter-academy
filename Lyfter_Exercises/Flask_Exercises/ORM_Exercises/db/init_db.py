from sqlalchemy import Engine, inspect

import app.models  # Registers every model in Base.metadata, DO NOT REMOVE
from app.config import get_config
from app.database import Base, create_db_engine


def find_missing_tables(engine: Engine) -> list[str]:
    inspector = inspect(engine)
    expected = [table.name for table in Base.metadata.sorted_tables]
    return [name for name in expected if not inspector.has_table(name)]

def main() -> None:
    config = get_config()
    engine = create_db_engine(config.DATABASE_URL, config.DB_SCHEMA)
    try:
        missing = find_missing_tables(engine)
        for table in Base.metadata.sorted_tables:
            status = "MISSING" if table.name in missing else "ok"
            print(f"{table.name:<16} {status}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    main()