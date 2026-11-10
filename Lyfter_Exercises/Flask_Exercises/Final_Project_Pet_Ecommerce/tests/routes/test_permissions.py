from http import HTTPStatus

import pytest
from flask.testing import FlaskClient

from app.security.permissions import ROLE_PERMISSIONS, UserRole

FORBIDDEN_DETAIL = "You don't have permission to perform this action."

ADMIN_ONLY_ENDPOINTS = [
    ("GET", "/api/v1/users"),
    ("DELETE", "/api/v1/users/{other_id}"),
    ("POST", "/api/v1/products"),
    ("PATCH", "/api/v1/products/1"),
    ("DELETE", "/api/v1/products/1"),
    ("PATCH", "/api/v1/products/1/restock"),
    ("GET", "/api/v1/login-history"),
]

@pytest.mark.parametrize(
    ("method", "path"),
    ADMIN_ONLY_ENDPOINTS,
    ids=[f"{method} {path}" for method, path in ADMIN_ONLY_ENDPOINTS],
)
def test_admin_endpoint_called_by_client_returns_403(client: FlaskClient, client_headers: dict, other_user: dict, method: str, path: str) -> None:
    url = path.format(other_id=other_user["user"]["id"])
    response = client.open(url, method=method, headers=client_headers)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.get_json()["detail"] == FORBIDDEN_DETAIL

def test_promoted_user_existing_token_gets_admin_access(client: FlaskClient, admin_headers: dict) -> None:
    response = client.get("/api/v1/users", headers=admin_headers)
    assert response.status_code == HTTPStatus.OK

def test_me_for_admin_returns_admin_role_and_its_permissions(client: FlaskClient, admin_headers: dict) -> None:
    data = client.get("/api/v1/auth/me", headers=admin_headers).get_json()["data"]
    assert data["role"] == "admin"
    assert data["permissions"] == sorted(ROLE_PERMISSIONS[UserRole.ADMIN])

def test_me_for_client_returns_client_role_and_its_permissions(client: FlaskClient, client_headers: dict) -> None:
    data = client.get("/api/v1/auth/me", headers=client_headers).get_json()["data"]
    assert data["role"] == "client"
    assert data["permissions"] == sorted(ROLE_PERMISSIONS[UserRole.CLIENT])

def test_client_can_list_products(client: FlaskClient, client_headers: dict) -> None:
    response = client.get("/api/v1/products", headers=client_headers)
    assert response.status_code == HTTPStatus.OK