from http import HTTPStatus

import pytest
from flask.testing import FlaskClient

from tests.routes.helpers.products import product_body, PRODUCTS_URL


@pytest.fixture
def product(client: FlaskClient, admin_headers: dict) -> dict:
    """ Creates a product. """
    response = client.post(PRODUCTS_URL, json=product_body(), headers=admin_headers)
    assert response.status_code == HTTPStatus.CREATED, response.get_json()
    return response.get_json()["data"]


@pytest.fixture
def stocked_product(client: FlaskClient, admin_headers: dict, product: dict) -> dict:
    """ The product fixture with 10 units of stock, added through the restock endpoint. """
    response = client.patch(f"{PRODUCTS_URL}/{product['id']}/restock", json={"stock": "10"}, headers=admin_headers)
    assert response.status_code == HTTPStatus.OK, response.get_json()
    return response.get_json()["data"]