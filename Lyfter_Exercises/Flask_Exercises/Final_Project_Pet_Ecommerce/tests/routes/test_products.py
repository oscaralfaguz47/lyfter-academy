from http import HTTPStatus

import pytest

from flask.testing import FlaskClient
from decimal import Decimal

from tests.routes.helpers.products import product_body, PRODUCT_FIELDS, PRODUCTS_URL


# ---------- HTTP POST create product ----------

def test_create_product_as_admin_returns_201_with_zero_stock_and_location(client: FlaskClient, admin_user: dict, admin_headers: dict) -> None:
    response = client.post(PRODUCTS_URL, json=product_body(), headers=admin_headers)

    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()["data"]
    assert set(data) == PRODUCT_FIELDS
    assert data["name"] == "Carrots"
    assert data["price"] == "5.50"
    assert data["stock"] == "0.000"
    assert data["created_by_id"] == admin_user["user"]["id"]
    assert response.headers["Location"] == f"{PRODUCTS_URL}/{data["id"]}"


def test_create_product_with_duplicated_name_returns_409(client: FlaskClient, admin_headers: dict, product: dict) -> None:
    response = client.post(PRODUCTS_URL, json=product_body(name=product["name"], price="9.99"), headers=admin_headers)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.get_json()["detail"] == "A product with this name already exists."
    assert client.get(PRODUCTS_URL, headers=admin_headers).get_json()["data"] == [product]


@pytest.mark.parametrize(
    ("overrides", "field"),
    [
        ({"name": "a" * 31}, "name"),
        ({"name": ""}, "name"),
        ({"price": "123456789.50"}, "price"),
        ({"price": "645.475"}, "price"),
        ({"price": "abcd"}, "price"),
        ({"price": "0"}, "price"),
        ({"price": "-1"}, "price"),
        ({"stock": "5"}, "stock"),
    ],
    ids=["name_31_chars", "name_empty", "price_11_digits", "price_3_decimals", "price_not_a_number", "price_zero", "price_negative", "stock_not_allowed"],
)
def test_create_product_with_invalid_parameters_returns_422_and_creates_nothing(client: FlaskClient, admin_headers: dict, overrides: dict, field: str) -> None:
    response = client.post(PRODUCTS_URL, json=product_body(**overrides), headers=admin_headers)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    body = response.get_json()
    assert body["detail"] == "The request body has invalid fields."
    assert body["errors"].keys() == {field}

    get_response = client.get(PRODUCTS_URL, headers=admin_headers)

    assert get_response.status_code == HTTPStatus.OK
    assert get_response.get_json()["data"] == []


# ---------- HTTP GET product by id ----------

def test_get_product_as_client_returns_200_with_the_created_product(client: FlaskClient, client_headers: dict, product: dict) -> None:
    response = client.get(f"{PRODUCTS_URL}/{product["id"]}", headers=client_headers)

    assert response.status_code == HTTPStatus.OK
    assert response.get_json()["data"] == product


def test_get_unknown_product_returns_404_with_its_id(client: FlaskClient, client_headers: dict) -> None:
    response = client.get(f"{PRODUCTS_URL}/999999", headers=client_headers)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json()["detail"] == "Product 999999 not found."

# ---------- HTTP GET get products list ----------

def test_list_products_as_client_returns_200_with_meta(client: FlaskClient, client_headers: dict, product: dict) -> None:
    response = client.get(PRODUCTS_URL, headers=client_headers)

    assert response.status_code == HTTPStatus.OK
    assert response.get_json()["data"] == [product] 
    assert response.get_json()["meta"] == {"page": 1, "per_page": 20, "total": 1, "total_pages": 1}


# ---------- HTTP PATCH update product ----------

def test_update_product_price_returns_200_and_keeps_other_fields(client: FlaskClient, admin_user: dict, admin_headers: dict, product: dict) -> None:
    url = f"{PRODUCTS_URL}/{product["id"]}"
    client.get(url, headers=admin_headers) # warm the cache

    # When an update is executed the cache must be invalidated
    response = client.patch(url, json=product_body(price="20.90"), headers=admin_headers)

    assert response.status_code == HTTPStatus.OK
    updated = response.get_json()["data"]
    assert updated == product | {
        "price": "20.90",
        "updated_by_id": admin_user["user"]["id"],
        "updated_at": updated["updated_at"]
    }
    # Here we also validate if the cache was invalidate
    assert client.get(url, headers=admin_headers).get_json()["data"] == updated


def test_update_product_stock_returns_422_and_changes_nothing(client: FlaskClient, admin_headers: dict, product: dict) -> None:
    url = f"{PRODUCTS_URL}/{product["id"]}"
    response = client.patch(url, json={"stock": "10"}, headers=admin_headers)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.get_json()["errors"].keys() == {"stock"} # We validate de keys and do not the Pydantic message
    assert client.get(url, headers=admin_headers).get_json()["data"] == product


# ---------- HTTP PATCH restock product ----------

def test_restock_twice_returns_200_and_adds_both_quantities(client: FlaskClient, admin_headers: dict, product: dict) -> None:
    url = f"{PRODUCTS_URL}/{product["id"]}/restock"
    first = client.patch(url, json={"stock": "10.50"}, headers=admin_headers)
    assert first.status_code == HTTPStatus.OK, first.get_json()

    response = client.patch(url, json={"stock": "20.5"}, headers=admin_headers)
    assert response.status_code == HTTPStatus.OK
    assert response.get_json()["data"]["stock"] == "31.000"


def test_restock_unknown_product_returns_404_with_its_id(client: FlaskClient, admin_headers: dict) -> None:
    response = client.patch(f"{PRODUCTS_URL}/9999999/restock", json={"stock": "10.55"}, headers=admin_headers)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json()["detail"] == "Product 9999999 not found."

# ---------- HTTP DELETE product ----------

def test_delete_unknown_product_returns_404_not_found(client: FlaskClient, admin_headers: dict) -> None:
    response = client.delete(f"{PRODUCTS_URL}/9999999", headers=admin_headers)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json()["detail"] == "Product 9999999 not found."