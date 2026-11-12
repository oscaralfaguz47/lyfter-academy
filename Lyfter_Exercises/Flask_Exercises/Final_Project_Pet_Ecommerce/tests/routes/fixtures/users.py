import pytest 

from http import HTTPStatus
from flask import Flask
from flask.testing import FlaskClient

from tests.routes.helpers.users import registration_body, ADMIN_EMAIL, OTHER_EMAIL, bearer

@pytest.fixture
def registered_user(client: FlaskClient) -> dict:
    return _register(client)

@pytest.fixture
def client_headers(registered_user: dict) -> dict[str, str]:
    return bearer(registered_user["access_token"])

@pytest.fixture
def other_user(client: FlaskClient) -> dict:
    return _register(client, name="Emilio Client", email=OTHER_EMAIL)

@pytest.fixture
def other_client_headers(other_user: dict) -> dict[str, str]:
    return bearer(other_user["access_token"])

@pytest.fixture
def admin_user(app: Flask, client: FlaskClient) -> dict:
    user = _register(client, name="Maria Admin", email=ADMIN_EMAIL)
    result = app.test_cli_runner().invoke(args=["promote-admin", ADMIN_EMAIL])
    assert result.exit_code == 0, result.output
    return user

@pytest.fixture
def admin_headers(admin_user: dict) -> dict[str, str]:
    return bearer(admin_user["access_token"])


def _register(client: FlaskClient, **overrides: object) -> dict:
    response = client.post("/api/v1/auth/register", json=registration_body(**overrides))
    assert response.status_code == HTTPStatus.CREATED, response.get_json()
    return response.get_json()["data"]