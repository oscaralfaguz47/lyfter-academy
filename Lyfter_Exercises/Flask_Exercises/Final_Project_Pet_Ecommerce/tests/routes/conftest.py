""" Fixtures for tests that go through HTTP against the real test database and Redis. """

from http import HTTPStatus
from collections.abc import Iterator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from redis import Redis
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app import create_app, models
from app.database import Base
from tests.routes.helpers import registration_body


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

@pytest.fixture
def registered_user(client: FlaskClient) -> dict:
    response = client.post("/api/v1/auth/register", json=registration_body())
    assert response.status_code == HTTPStatus.CREATED, response.get_json()
    return response.get_json()["data"]

@pytest.fixture
def db_session(app: Flask) -> Iterator[Session]:
    session = app.extensions["db_session_factory"]()
    yield session
    session.close()


def _ensure_test_database(engine: Engine) -> None:
    name = engine.url.database or ""
    if not name.endswith("_test"):
        raise RuntimeError(f"Refusing to run tests against database '{name}': its name must end with '_test'.")

def _ensure_test_redis(client: Redis) -> None:
    if client.connection_pool.connection_kwargs.get("db", 0) == 0:
        raise RuntimeError("Refusing to run tests against Redis db 0: use another number in TEST_REDIS_URL.")