""" Fixtures for tests that go through HTTP against the real test database and Redis. """

from collections.abc import Iterator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from redis import Redis
from sqlalchemy import Engine

from app import create_app, models
from app.database import Base

@pytest.fixture(scope="session")
def app() -> Iterator[Flask]:
    app = create_app("testing")
    engine: Engine = app.extensions["db_engine"]
    _ensure_test_database(engine)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield app
    Base.metadata.drop_all(engine)
    engine.dispose()

@pytest.fixture(scope="session")
def redis_client(app: Flask) -> Iterator[Redis]:
    client = Redis.from_url(app.config["REDIS_URL"], decode_responses=True)
    _ensure_test_redis(client)
    yield client
    client.close()

@pytest.fixture(autouse=True)
def clean_state(app: Flask, redis_client: Redis) -> None:
    with app.extensions["db_engine"].begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())
    redis_client.flushdb()

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()



def _ensure_test_database(engine: Engine) -> None:
    name = engine.url.database or ""
    if not name.endswith("_test"):
        raise RuntimeError(f"Refusing to run tests against database '{name}': its name must end with '_test'.")

def _ensure_test_redis(client: Redis) -> None:
    if client.connection_pool.connection_kwargs.get("db", 0) == 0:
        raise RuntimeError("Refusing to run tests against Redis db 0: use another number in TEST_REDIS_URL.")