from http import HTTPStatus

import pytest
from flask.testing import FlaskClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import LoginHistory
from tests.routes.helpers.users import login_body, PUBLIC_USER_FIELDS

USERS_URL = "/api/v1/users"
LOGIN_URL = "/api/v1/auth/login"

# ---------- OWN ACCOUNT AS CLIENT ----------

def test_get_own_user_as_client_returns_200_with_own_account(client: FlaskClient, registered_user: dict, client_headers: dict) -> None:
    user_id = registered_user["user"]["id"]
    response = client.get(f"{USERS_URL}/{user_id}", headers=client_headers)
    assert response.status_code == HTTPStatus.OK    
    assert response.get_json()["data"] == registered_user["user"]

def test_update_own_user_as_client_returns_200_and_saves(client: FlaskClient, registered_user: dict, client_headers: dict) -> None:
    url = f"{USERS_URL}/{registered_user["user"]["id"]}"
    response = client.patch(url, json={"phone_number": "+506 2222-4444"}, headers=client_headers)
    data = response.get_json()["data"]
    assert response.status_code == HTTPStatus.OK
    assert set(data) == PUBLIC_USER_FIELDS
    assert data["phone_number"] == "+506 2222-4444"
    assert client.get(url, headers=client_headers).get_json()["data"]["phone_number"] == "+506 2222-4444"

@pytest.mark.parametrize("method", ["GET", "PATCH"])
def test_other_user_as_client_returns_404_and_changes_nothing(client: FlaskClient, client_headers: dict, other_user: dict, other_client_headers: dict, method: str) -> None:
    other_id = other_user["user"]["id"]
    response = client.open(f"{USERS_URL}/{other_id}", method=method, json={"name": "Hacked"}, headers=client_headers)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json()["detail"] == f"User {other_id} not found."
    own_view = client.get(f"{USERS_URL}/{other_id}", headers=other_client_headers).get_json()["data"]
    assert own_view["name"] == "Emilio Client"

def test_delete_own_user_as_client_returns_403(client: FlaskClient, registered_user: dict, client_headers: dict) -> None:
    response = client.delete(f"{USERS_URL}/{registered_user["user"]["id"]}", headers=client_headers)
    assert response.status_code == HTTPStatus.FORBIDDEN

@pytest.mark.parametrize("field", ["name", "email", "phone_number"])
def test_update_own_user_with_null_field_returns_422_and_changes_nothing(client: FlaskClient, registered_user: dict, client_headers: dict, field: str) -> None:
    url = f"{USERS_URL}/{registered_user["user"]["id"]}"
    response = client.patch(url, json={field: None}, headers=client_headers)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert list(response.get_json()["errors"]) == [field]
    saved = client.get(url, headers=client_headers).get_json()["data"]
    assert saved[field] == registered_user["user"][field]

@pytest.mark.parametrize("headers_fixture", ["client_headers", "admin_headers"])
def test_update_user_with_role_returns_422_and_keeps_role(client: FlaskClient, registered_user: dict, headers_fixture: str, request: pytest.FixtureRequest) -> None:
    headers = request.getfixturevalue(headers_fixture)
    url = f"{USERS_URL}/{registered_user["user"]["id"]}"
    response = client.patch(url, json={"role": "admin"}, headers=headers)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert list(response.get_json()["errors"]) == ["role"]
    saved = client.get(url, headers=headers).get_json()["data"]
    assert saved["role"] == "client"

def test_delete_user_who_created_a_product_returns_409_and_keeps_user(client: FlaskClient, admin_user: dict, admin_headers: dict) -> None:
    client.post("/api/v1/products", json={"name": "Watermelon", "price": "10.5"}, headers=admin_headers)
    url = f"{USERS_URL}/{admin_user["user"]["id"]}"
    response = client.delete(url, headers=admin_headers)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.get_json()["detail"] == f"User {admin_user["user"]["id"]} has products or invoices that reference them."
    assert client.get(url, headers=admin_headers).status_code == HTTPStatus.OK

def test_delete_user_without_sales_returns_204_and_keeps_login_history(client: FlaskClient, registered_user: dict, admin_headers: dict, db_session: Session) -> None:
    client.post(LOGIN_URL, json=login_body())
    url = f"{USERS_URL}/{registered_user["user"]["id"]}"
    response = client.delete(url, headers=admin_headers)
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert client.get(url, headers=admin_headers).status_code == HTTPStatus.NOT_FOUND
    rows = db_session.scalars(select(LoginHistory)).all()
    assert [(row.user_id, row.success) for row in rows] == [(None, True)]