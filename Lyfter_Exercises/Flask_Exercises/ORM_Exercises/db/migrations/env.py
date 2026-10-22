""" Alembic environment: tells Alembic how to connect and which models to compare. """

from logging.config import fileConfig

from alembic import context

import app.models # Triggers the registry from 5.2, so every model lands Base.metadata
from app.config import get_config
from app.database import Base, create_db_engine

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Same APP_ENV and .env as the app, reuses our config class
app_config = get_config() 
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=app_config.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """ Connect to the db and run the migrations """
    engine = create_db_engine(app_config.DATABASE_URL, app_config.DB_SCHEMA)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    # Closes the pool when Alembic finishes
    engine.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()