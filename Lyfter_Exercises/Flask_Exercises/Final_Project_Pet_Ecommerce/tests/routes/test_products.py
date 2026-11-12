from http import HTTPStatus

import pytest

from flask.testing import FlaskClient

from tests.routes.helpers.products import product_body, PRODUCT_FIELDS, PRODUCTS_URL


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


def test_get_product_as_client_returns_200_with_the_created_product(client: FlaskClient, client_headers: dict, product: dict) -> None:
    response = client.get(f"{PRODUCTS_URL}/{product["id"]}", headers=client_headers)

    assert response.status_code == HTTPStatus.OK
    assert response.get_json()["data"] == product


def test_list_products_as_client_returns_200_with_meta(client: FlaskClient, client_headers: dict, product: dict) -> None:
    response = client.get(PRODUCTS_URL, headers=client_headers)

    assert response.status_code == HTTPStatus.OK
    assert response.get_json()["data"] == [product] 
    assert response.get_json()["meta"] == {"page": 1, "per_page": 20, "total": 1, "total_pages": 1}


def test_get_unknown_product_returns_404_with_its_id(client: FlaskClient, client_headers: dict) -> None:
    response = client.get(f"{PRODUCTS_URL}/999999", headers=client_headers)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json()["detail"] == "Product 999999 not found."


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
    