from http import HTTPStatus

import pytest
from flask.testing import FlaskClient

USERS_URL = "/api/v1/users"

# ---------- OWN ACCOUNT AS CLIENT ----------

def test_get_own_user_as_client_returns_200(client: FlaskClient, registered_user: dict, client_headers: dict) -> None:
    user_id = registered_user["user"]["id"]
    response = client.get(f"{USERS_URL}/{user_id}", headers=client_headers)
    assert response.status_code == HTTPStatus.OK    
    assert response.get_json()["data"]["id"] == user_id

def test_update_own_user_as_client_returns_200_and_saves(client: FlaskClient, registered_user: dict, client_headers: dict) -> None:
    url = f"{USERS_URL}/{registered_user["user"]["id"]}"
    response = client.patch(url, json={"phone_number": "+506 2222-4444"}, headers=client_headers)
    assert response.status_code == HTTPStatus.OK
    assert response.get_json()["data"]["phone_number"] == "+506 2222-4444"
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