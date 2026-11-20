from http import HTTPStatus

import pytest
from flask.testing import FlaskClient

from tests.routes.helpers.cart import CHECKOUT_URL, checkout_body, item_url

@pytest.fixture
def cart_with_item(client: FlaskClient, client_headers: dict, stocked_product: dict) -> dict:
    """ registered_user's cart with 2 units of stocked_product. """
    response = client.put(item_url(stocked_product["id"]), json={"quantity": "2"}, headers=client_headers)
    assert response.status_code == HTTPStatus.OK, response.get_json()
    return response.get_json()["data"]

@pytest.fixture
def paid_invoice(client: FlaskClient, client_headers: dict, cart_with_item: dict) -> dict:
    """ The invoice from checking out cart_with_item. """
    response = client.post(CHECKOUT_URL, json=checkout_body(), headers=client_headers)
    assert response.status_code == HTTPStatus.CREATED, response.get_json()
    return response.get_json()["data"]
