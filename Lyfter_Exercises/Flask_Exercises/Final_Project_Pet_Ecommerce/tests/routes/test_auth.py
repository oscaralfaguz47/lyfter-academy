import base64
import json
from datetime import timedelta
import jwt
import pytest
from http import HTTPStatus
from flask import Flask
from flask.testing import FlaskClient
from flask.wrappers import Response
from sqlalchemy import select
from sqlalchemy.orm import Session


from app.models import LoginHistory
from tests.routes.helpers.users import EMAIL, bearer, registration_body, login_body, PUBLIC_USER_FIELDS
from app.security.tokens import TokenService

REGISTER_URL = "api/v1/auth/register"
ME_URL = "api/v1/auth/me"

LOGIN_URL = "/api/v1/auth/login"
TOKEN_FIELDS = {"access_token", "refresh_token", "token_type", "expires_in"}

REFRESH_URL = "/api/v1/auth/refresh-token"
LOGOUT_URL = "/api/v1/auth/logout"


# ---------- REGISTER ---------

def test_register_with_valid_data_returns_201_and_client_user(app: Flask, client: FlaskClient) -> None:
    response = client.post(REGISTER_URL, json=registration_body())

    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()["data"]
    user = data["user"]
    assert set(user) == PUBLIC_USER_FIELDS
    assert user["name"] == "Oscar Alfaro Client"
    assert user["email"] == "oscar.alfaro@example.com"
    assert user["phone_number"] == "+506 85318674"
    assert user["role"] == "client"
    assert response.headers["Location"] == f"/api/v1/users/{user['id']}"
    assert data["token_type"] == "Bearer"
    assert data["expires_in"] == app.config["JWT_ACCESS_TOKEN_MINUTES"] * 60

def test_register_returns_an_access_token_that_works(client: FlaskClient) -> None:
    tokens = client.post(REGISTER_URL, json=registration_body()).get_json()["data"]
    response = client.get(ME_URL, headers=bearer(tokens["access_token"]))
    assert response.status_code == HTTPStatus.OK
    assert response.get_json()["data"]["email"] == "oscar.alfaro@example.com"

def test_register_normalizes_email_and_strips_name(client: FlaskClient) -> None:
    body = registration_body(name=" Oscar Alfaro Client ", email="oscar.alfaro@example.com")
    response = client.post(REGISTER_URL, json=body)
    user = response.get_json()["data"]["user"]
    assert user["name"] == "Oscar Alfaro Client"
    assert user["email"] == "oscar.alfaro@example.com"

@pytest.mark.parametrize("email", ["oscar.alfaro@example.com", "OSCAR.alfaro@EXAMPLE.com"], ids=["same", "different_case"])
def test_register_with_existing_email_returns_409(client: FlaskClient, email: str) -> None:
    client.post(REGISTER_URL, json=registration_body())
    response = client.post(REGISTER_URL, json=registration_body(email=email))
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.content_type == "application/problem+json"
    assert response.get_json()["detail"] == "A user with email oscar.alfaro@example.com already exists."

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


# ---------- LOGIN ---------

def test_login_with_valid_credentials_returns_200_and_working_tokens(client: FlaskClient, registered_user: dict) -> None:
    response = client.post(LOGIN_URL, json=login_body())

    assert response.status_code == HTTPStatus.OK
    data = response.get_json()["data"]
    assert set(data) == TOKEN_FIELDS
    assert client.get(ME_URL, headers=bearer(data["access_token"])).status_code == HTTPStatus.OK
def test_login_with_email_in_other_case_returns_200(client: FlaskClient, registered_user: dict) -> None:
    response = client.post(LOGIN_URL, json=login_body(email=EMAIL.upper()))
    assert response.status_code == HTTPStatus.OK

@pytest.mark.parametrize("overrides",[
    {"password": "my_wrong-password"}, {"email": "nobody@example.com"}
], ids=["wrong_password", "unknown_email"],)
def test_login_with_bad_credentials_returns_401_with_same_detail(client: FlaskClient, registered_user: dict, overrides: dict) -> None:
    response =client.post(LOGIN_URL, json=login_body(**overrides))
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.get_json()["detail"] == "Invalid email or password."

def test_login_saves_every_attempt_in_history(client: FlaskClient, registered_user: dict, db_session: Session) -> None:
    client.post(LOGIN_URL, json=login_body())
    client.post(LOGIN_URL, json=login_body(password="wrong-password"))
    client.post(LOGIN_URL, json=login_body(email="no-registered-email@example.com"))
    rows = db_session.scalars(select(LoginHistory).order_by(LoginHistory.id)).all()
    user_id = registered_user["user"]["id"]
    assert [(row.user_id, row.success) for row in rows] == [(user_id, True), (user_id, False), (None, False)]
    assert all(str(row.user_ip) == "127.0.0.1" for row in rows)

def test_login_without_password_returns_422(client: FlaskClient) -> None:
    response = client.post(LOGIN_URL, json={"email": EMAIL})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert list(response.get_json()["errors"]) == ["password"]


# ---------- ACCESS TOKEN ---------

@pytest.mark.parametrize(
        "headers",
        [{}, {"Authorization": "Basic abc123"}, {"Authorization": "Bearer "}],
        ids=["missing", "wrong_scheme", "empty_token"],
)
def test_me_without_valid_authorization_header_returns_401(client: FlaskClient, headers: dict) -> None:
    response = client.get(ME_URL, headers=headers)
    _assert_unauthorized(response, "Missing or malformed Authorization header. Use: Bearer <token>")

def test_me_with_expired_token_returns_401(app: Flask, client: FlaskClient, registered_user: dict) -> None:
    user_id = registered_user["user"]["id"]
    token = _token_service(app, timedelta(seconds=-1)).create_pair(user_id, version=0).access_token
    response = client.get(ME_URL, headers=bearer(token))
    _assert_unauthorized(response, "Token has expired.")

def test_me_with_token_forged_for_another_user_returns_401(client: FlaskClient, registered_user: dict) -> None:
    victim = client.post(REGISTER_URL, json=registration_body(email="emilio@example.com")).get_json()["data"]
    forged = _with_subject(registered_user["access_token"], str(victim["user"]["id"]))
    response = client.get(ME_URL, headers=bearer(forged))
    _assert_unauthorized(response, "Invalid token.")

def test_me_with_unsigned_token_returns_401(client: FlaskClient, registered_user: dict) -> None:
    claims = jwt.decode(registered_user["access_token"], options={"verify_signature": False})
    unsigned = jwt.encode(claims, None, algorithm="none")
    response = client.get(ME_URL, headers=bearer(unsigned))
    _assert_unauthorized(response, "Invalid token.")

def test_me_with_refresh_token_returns_401(client: FlaskClient, registered_user: dict) -> None:
    response = client.get(ME_URL, headers=bearer(registered_user["refresh_token"]))
    _assert_unauthorized(response, "Invalid token.")

# ---------- REFRESH ---------

def test_refresh_with_valid_refresh_token_returns_200_and_working_tokens(client: FlaskClient, registered_user: dict) -> None:
    response = client.post(REFRESH_URL, json={"refresh_token": registered_user["refresh_token"]})
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()["data"]
    assert set(data) == TOKEN_FIELDS
    assert client.get(ME_URL, headers=bearer(data["access_token"])).status_code == HTTPStatus.OK

def test_refresh_with_access_token_returns_401(client: FlaskClient, registered_user: dict) -> None:
    response = client.post(REFRESH_URL, json={"refresh_token": registered_user["access_token"]})
    _assert_unauthorized(response, "Invalid token.")

# ---------- LOGOUT ---------

def test_logout_returns_204_and_revokes_both_tokens(client: FlaskClient, registered_user: dict) -> None:
    headers = bearer(registered_user["access_token"])
    response = client.post(LOGOUT_URL, headers=headers)
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.data == b""
    _assert_unauthorized(client.get(ME_URL, headers=headers), "Invalid token.")
    refresh = client.post(REFRESH_URL, json={"refresh_token": registered_user["refresh_token"]})
    _assert_unauthorized(refresh, "Invalid token.")

def test_logout_revokes_tokens_on_every_device(client: FlaskClient, registered_user: dict) -> None:
    other_device = client.post(LOGIN_URL, json=login_body()).get_json()["data"]
    client.post(LOGOUT_URL, headers=bearer(registered_user["access_token"]))
    _assert_unauthorized(client.get(ME_URL, headers=bearer(other_device["access_token"])), "Invalid token.")

def test_login_after_logout_returns_working_tokens(client: FlaskClient, registered_user: dict) -> None:
    client.post(LOGOUT_URL, headers=bearer(registered_user["access_token"]))
    tokens = client.post(LOGIN_URL, json=login_body()).get_json()["data"]
    assert client.get(ME_URL, headers=bearer(tokens["access_token"])).status_code == HTTPStatus.OK



# ---------- HELPERS ---------

def _assert_unauthorized(response: Response, detail: str) -> None:
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.get_json()["detail"] == detail

def _token_service(app: FlaskClient, access_lifetime: timedelta) -> TokenService:
    return TokenService(
        private_key=app.config["JWT_PRIVATE_KEY"],
        public_key=app.config["JWT_PUBLIC_KEY"],
        access_lifetime=access_lifetime,
        refresh_lifetime=timedelta(days=1)
    )

def _with_subject(token: str, subject: str) -> str:
    """ Change the payload but keep the original signature, like an attacker would. """
    header, payload, signature = token.split(".")
    claims = json.loads(base64.urlsafe_b64decode(payload + "=="))
    claims["sub"] = subject
    forged = base64.urlsafe_b64encode(json.dumps(claims).encode()).rstrip(b"=").decode()
    return f"{header}.{forged}.{signature}"