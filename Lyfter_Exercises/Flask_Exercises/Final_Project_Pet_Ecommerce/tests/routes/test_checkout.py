from http import HTTPStatus

from flask.testing import FlaskClient

from tests.routes.helpers.cart import BILLING, CART_URL, CHECKOUT_URL, EMPTY_CART, checkout_body, item_url
from tests.routes.helpers.products import PRODUCTS_URL


def test_checkout_returns_201_with_the_invoice_reduces_stock_and_empties_the_cart(
        client: FlaskClient, client_headers: dict, admin_headers: dict, stocked_product: dict, cart_with_item: dict) -> None:
    response = client.post(CHECKOUT_URL, json=checkout_body(), headers=client_headers)

    assert response.status_code == HTTPStatus.CREATED
    invoice = response.get_json()["data"]
    assert response.headers["Location"] == f"/api/v1/invoices/{invoice['invoice_number']}"
    assert invoice["status"] == "paid"
    assert invoice["total_amount"] == "11.00"
    assert [(line["product_id"], line["product_name"], line["quantity"], line["price"]) for line in invoice["invoice_lines"]] == [
        (stocked_product["id"], "Carrots", "2.000", "5.50")
    ]
    assert invoice["billing"] == BILLING
    assert invoice["payment"] == {"method": "sinpe", "reference": "20261105123456"}

    stock = client.get(f"{PRODUCTS_URL}/{stocked_product['id']}", headers=admin_headers).get_json()["data"]["stock"]
    assert stock == "8.000"
    assert client.get(CART_URL, headers=client_headers).get_json()["data"] == EMPTY_CART


def test_checkout_without_cart_returns_409(client: FlaskClient, client_headers: dict) -> None:
    response = client.post(CHECKOUT_URL, json=checkout_body(), headers=client_headers)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.get_json()["detail"] == "Your cart is empty."


def test_checkout_without_enough_stock_returns_409_and_saves_nothing(
        client: FlaskClient, client_headers: dict, other_client_headers: dict, stocked_product: dict) -> None:
    # Both users want the 10 units, the other user buys them first
    client.put(item_url(stocked_product["id"]), json={"quantity": "10"}, headers=client_headers)
    client.put(item_url(stocked_product["id"]), json={"quantity": "10"}, headers=other_client_headers)
    assert client.post(CHECKOUT_URL, json=checkout_body(), headers=other_client_headers).status_code == HTTPStatus.CREATED

    response = client.post(CHECKOUT_URL, json=checkout_body(), headers=client_headers)

    assert response.status_code == HTTPStatus.CONFLICT
    body = response.get_json()
    assert body["detail"] == "Not enough stock."
    assert body["errors"] == {"products": [{"product_id": stocked_product["id"], "requested": "10.000", "available": "0.000"}]}
    assert client.get("/api/v1/invoices", headers=client_headers).get_json()["meta"]["total"] == 0
    assert len(client.get(CART_URL, headers=client_headers).get_json()["data"]["cart_items"]) == 1


def test_checkout_with_full_card_number_returns_422_and_keeps_the_cart(
        client: FlaskClient, client_headers: dict, cart_with_item: dict) -> None:
    body = checkout_body(method="card", reference="4111111111111111")

    response = client.post(CHECKOUT_URL, json=body, headers=client_headers)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.get_json()["errors"] == {"payment": ["For card payments, reference must be exactly the last 4 digits."]}
    assert client.get(CART_URL, headers=client_headers).get_json()["data"] == cart_with_item


def test_checkout_twice_returns_409_the_second_time(client: FlaskClient, client_headers: dict, paid_invoice: dict) -> None:
    response = client.post(CHECKOUT_URL, json=checkout_body(), headers=client_headers)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.get_json()["detail"] == "Your cart is empty."