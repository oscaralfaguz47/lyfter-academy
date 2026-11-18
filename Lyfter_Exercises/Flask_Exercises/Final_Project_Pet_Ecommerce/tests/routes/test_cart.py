from http import HTTPStatus

import pytest
from flask.testing import FlaskClient

from tests.routes.helpers.cart import CART_URL, EMPTY_CART, item_url


# ---------- HTTP GET cart ----------

def test_get_cart_without_cart_returns_empty_cart(client: FlaskClient, client_headers: dict) -> None:
    response = client.get(CART_URL, headers=client_headers)

    assert response.status_code == HTTPStatus.OK
    assert response.get_json()["data"] == EMPTY_CART

# ---------- HTTP PUT cart item ----------

def test_set_item_returns_200_with_the_item_and_its_total(client: FlaskClient, client_headers: dict, stocked_product: dict) -> None:
    response = client.put(item_url(stocked_product["id"]), json={"quantity": "2"}, headers=client_headers)

    assert response.status_code == HTTPStatus.OK
    cart = response.get_json()["data"]
    assert cart == {
        "cart_items": [
            {"product": {"id": stocked_product["id"], "name": "Carrots", "price": "5.50"}, "quantity": "2.000", "total_amount": "11.00"}
        ],
        "total_amount": "11.00",
    }
    assert client.get(CART_URL, headers=client_headers).get_json()["data"] == cart


def test_set_item_twice_replaces_the_quantity(client: FlaskClient, client_headers: dict, stocked_product: dict) -> None:
    client.put(item_url(stocked_product["id"]), json={"quantity": "2"}, headers=client_headers)
    response = client.put(item_url(stocked_product["id"]), json={"quantity": "5"}, headers=client_headers)

    assert response.status_code == HTTPStatus.OK
    items = response.get_json()["data"]["cart_items"]
    assert [(item["product"]["id"], item["quantity"]) for item in items] == [(stocked_product["id"], "5.000")]


def test_set_item_over_stock_returns_409_and_leaves_the_cart_empty(client: FlaskClient, client_headers: dict, stocked_product: dict) -> None:
    response = client.put(item_url(stocked_product["id"]), json={"quantity": "11"}, headers=client_headers)

    assert response.status_code == HTTPStatus.CONFLICT
    body = response.get_json()
    assert body["detail"] == "Not enough stock."
    assert body["errors"] == {"products": [{"product_id": stocked_product["id"], "requested": "11", "available": "10.000"}]}
    assert client.get(CART_URL, headers=client_headers).get_json()["data"] == EMPTY_CART


@pytest.mark.parametrize("quantity", ["0", "-1", "1.2345"], ids=["zero", "negative", "4_decimals"])
def test_set_item_with_invalid_quantity_returns_422(client: FlaskClient, client_headers: dict, stocked_product: dict, quantity: str) -> None:
    response = client.put(item_url(stocked_product["id"]), json={"quantity": quantity}, headers=client_headers)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.get_json()["errors"].keys() == {"quantity"}

# ---------- HTTP DELETE cart item ----------

def test_remove_item_twice_returns_200_then_404(client: FlaskClient, client_headers: dict, stocked_product: dict) -> None:
    client.put(item_url(stocked_product["id"]), json={"quantity": "2"}, headers=client_headers)

    first = client.delete(item_url(stocked_product["id"]), headers=client_headers)
    second = client.delete(item_url(stocked_product["id"]), headers=client_headers)

    assert first.status_code == HTTPStatus.OK
    assert first.get_json()["data"] == EMPTY_CART
    assert second.status_code == HTTPStatus.NOT_FOUND
    assert second.get_json()["detail"] == f"Product {stocked_product['id']} is not in the cart."

# ---------- Ownership ----------

def test_other_user_cannot_see_or_remove_your_items(
        client: FlaskClient, client_headers: dict, other_client_headers: dict, stocked_product: dict) -> None:
    client.put(item_url(stocked_product["id"]), json={"quantity": "2"}, headers=client_headers)

    assert client.get(CART_URL, headers=other_client_headers).get_json()["data"] == EMPTY_CART
    assert client.delete(item_url(stocked_product["id"]), headers=other_client_headers).status_code == HTTPStatus.NOT_FOUND
    assert len(client.get(CART_URL, headers=client_headers).get_json()["data"]["cart_items"]) == 1