from http import HTTPStatus

from flask.testing import FlaskClient

INVOICES_URL = "/api/v1/invoices"
FORBIDDEN_DETAIL = "You don't have permission to perform this action."


def test_get_own_invoice_by_number_returns_200(client: FlaskClient, client_headers: dict, paid_invoice: dict) -> None:
    response = client.get(f"{INVOICES_URL}/{paid_invoice['invoice_number']}", headers=client_headers)

    assert response.status_code == HTTPStatus.OK
    assert response.get_json()["data"] == paid_invoice

def test_get_another_users_invoice_returns_404(client: FlaskClient, other_client_headers: dict, paid_invoice: dict) -> None:
    response = client.get(f"{INVOICES_URL}/{paid_invoice['invoice_number']}", headers=other_client_headers)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json()["detail"] == f"Invoice {paid_invoice['invoice_number']} not found."

def _returns_url(invoice: dict) -> str:
    return f"{INVOICES_URL}/{invoice['invoice_number']}/returns"

def _return_body(invoice: dict, quantity: str) -> dict:
    return {"reason": "Damaged packaging", "lines": [{"invoice_line_id": invoice["invoice_lines"][0]["id"], "quantity": quantity}]}


def test_partial_return_returns_201_refunds_the_invoice_price_and_restores_stock(
        client: FlaskClient, admin_headers: dict, paid_invoice: dict, stocked_product: dict) -> None:
    response = client.post(_returns_url(paid_invoice), json=_return_body(paid_invoice, "1"), headers=admin_headers)

    assert response.status_code == HTTPStatus.CREATED
    assert response.headers["Location"] == _returns_url(paid_invoice)
    invoice_return = response.get_json()["data"]
    assert invoice_return["refund_amount"] == "5.50"
    assert invoice_return["invoice_status"] == "paid"
    assert invoice_return["invoice_return_lines"] == [{"invoice_line_id": paid_invoice["invoice_lines"][0]["id"], "quantity": "1.000"}]
    stock = client.get(f"/api/v1/products/{stocked_product['id']}", headers=admin_headers).get_json()["data"]["stock"]
    assert stock == "9.000"


def test_return_everything_marks_the_invoice_returned(
        client: FlaskClient, admin_headers: dict, client_headers: dict, paid_invoice: dict) -> None:
    response = client.post(_returns_url(paid_invoice), json=_return_body(paid_invoice, "2"), headers=admin_headers)

    assert response.status_code == HTTPStatus.CREATED
    assert response.get_json()["data"]["invoice_status"] == "returned"
    invoice = client.get(f"{INVOICES_URL}/{paid_invoice['invoice_number']}", headers=client_headers).get_json()["data"]
    assert invoice["status"] == "returned"


def test_return_more_than_whats_left_returns_409(client: FlaskClient, admin_headers: dict, paid_invoice: dict) -> None:
    client.post(_returns_url(paid_invoice), json=_return_body(paid_invoice, "1"), headers=admin_headers)

    response = client.post(_returns_url(paid_invoice), json=_return_body(paid_invoice, "2"), headers=admin_headers)

    assert response.status_code == HTTPStatus.CONFLICT
    body = response.get_json()
    assert body["detail"] == "Not enough left to return."
    assert body["errors"] == {
        "lines": [{"invoice_line_id": paid_invoice["invoice_lines"][0]["id"], "requested": "2", "available": "1.000"}]
    }


def test_client_creating_a_return_returns_403(client: FlaskClient, client_headers: dict, paid_invoice: dict) -> None:
    response = client.post(_returns_url(paid_invoice), json=_return_body(paid_invoice, "1"), headers=client_headers)

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.get_json()["detail"] == FORBIDDEN_DETAIL