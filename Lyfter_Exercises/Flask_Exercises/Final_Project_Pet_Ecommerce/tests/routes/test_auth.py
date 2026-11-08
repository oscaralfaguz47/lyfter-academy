import pytest
from http import HTTPStatus
from flask import Flask
from flask.testing import FlaskClient

from tests.routes.helpers import bearer, registration_body

REGISTER_URL = "api/v1/auth/register"
ME_URL = "api/v1/auth/me"
PUBLIC_USER_FIELDS = {"id", "name", "phone_number", "email", "created_at", "updated_at", "role"}


# ---------- REGISTER ---------

def test_register_with_valid_data_returns_201_and_client_user(app: Flask, client: FlaskClient) -> None:
    response = client.post(REGISTER_URL, json=registration_body())

    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()["data"]
    user = data["user"]
    assert set(user) == PUBLIC_USER_FIELDS
    assert user["name"] == "Oscar Alfaro Client"
    assert user["email"] == "oscar.alfaro.test@gmail.com"
    assert user["phone_number"] == "+506 85318674"
    assert user["role"] == "client"
    assert response.headers["Location"] == f"/api/v1/users/{user['id']}"
    assert data["token_type"] == "Bearer"
    assert data["expires_in"] == app.config["JWT_ACCESS_TOKEN_MINUTES"] * 60

def test_register_returns_an_access_token_that_works(client: FlaskClient) -> None:
    tokens = client.post(REGISTER_URL, json=registration_body()).get_json()["data"]

    response = client.get(ME_URL, headers=bearer(tokens["access_token"]))

    assert response.status_code == HTTPStatus.OK
    assert response.get_json()["data"]["email"] == "oscar.alfaro.test@gmail.com"

def test_register_normalizes_email_and_strips_name(client: FlaskClient) -> None:
    body = registration_body(name=" Oscar Alfaro Client ", email="oscar.alfaro.test@gmail.com")

    response = client.post(REGISTER_URL, json=body)

    user = response.get_json()["data"]["user"]
    assert user["name"] == "Oscar Alfaro Client"
    assert user["email"] == "oscar.alfaro.test@gmail.com"

@pytest.mark.parametrize("email", ["oscar.alfaro.test@gmail.com", "OSCAR.alfaro.test@GMAIL.com"], ids=["same", "different_case"])
def test_register_with_existing_email_returns_409(client: FlaskClient, email: str) -> None:
    client.post(REGISTER_URL, json=registration_body())

    response = client.post(REGISTER_URL, json=registration_body(email=email))

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.content_type == "application/problem+json"
    assert response.get_json()["detail"] == "A user with email oscar.alfaro.test@gmail.com already exists."

@pytest.mark.parametrize("field", ["name", "email", "phone_number", "password"])
def test_register_without_required_field_returns_422(client: FlaskClient, field: str) -> None:
    body = registration_body()
    del body[field]

    response = client.post(REGISTER_URL, json=body)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert list(response.get_json()["errors"]) == [field]

@pytest.mark.parametrize(
    ("overrides", "field"),
    [
        ({"email": "is-not-an-email"}, "email"),
        ({"password": "x" * 7}, "password"),
        ({"name": " "}, "name"),
        ({"phone_number": "1" * 21}, "phone_number"),
        ({"role": "admin"}, "role"),
    ],
    ids=["bad_email", "password_7_chars", "blank_name", "phone_too_long", "role_not_allowed"],
)
def test_register_with_invalid_field_return_422(client: FlaskClient, overrides: dict, field: str) -> None:
    response = client.post(REGISTER_URL, json=registration_body(**overrides))

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    body = response.get_json()
    assert body["detail"] == "The request body has invalid fields."
    assert list(body["errors"]) == [field]

@pytest.mark.parametrize(
    ("request_kwargs", "expected_status"),
    [
        ({"data": "name=Oscar"}, HTTPStatus.UNSUPPORTED_MEDIA_TYPE),
        ({"data": "{bad json}", "content_type": "application/json"}, HTTPStatus.BAD_REQUEST),
    ],
    ids=["not_json", "malformed_json"],
)
def test_register_with_unreadable_body_return_4xx(client: FlaskClient, request_kwargs: dict, expected_status: HTTPStatus) -> None:
    response = client.post(REGISTER_URL, **request_kwargs)

    assert response.status_code == expected_status
    assert response.content_type == "application/problem+json"
