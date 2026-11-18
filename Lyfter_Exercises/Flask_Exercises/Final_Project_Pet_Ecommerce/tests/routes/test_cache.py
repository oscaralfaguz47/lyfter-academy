from http import HTTPStatus

from flask.testing import FlaskClient
from redis import Redis

INVOICES_URL = "/api/v1/invoices"



def test_get_invoice_twice_stores_it_in_redis_with_a_ttl(client: FlaskClient, client_headers: dict, redis_client: Redis, paid_invoice: dict) -> None:
    url = f"{INVOICES_URL}/{paid_invoice['invoice_number']}"
    key = f"invoices:v1:{paid_invoice['invoice_number']}"

    first = client.get(url, headers=client_headers)
    second = client.get(url, headers=client_headers)

    assert redis_client.exists(key) == 1
    assert 290 <= redis_client.ttl(key) <= 330  # 5 minutes plus up to 10% jitter
    assert first.get_json()["data"] == second.get_json()["data"] == paid_invoice


def test_cached_invoice_for_another_client_returns_404(client: FlaskClient, client_headers: dict, other_client_headers: dict, paid_invoice: dict) -> None:
    url = f"{INVOICES_URL}/{paid_invoice['invoice_number']}"
    client.get(url, headers=client_headers)  # Now it's cached

    response = client.get(url, headers=other_client_headers)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_two_clients_with_the_same_params_see_their_own_list(client: FlaskClient, client_headers: dict, other_client_headers: dict, paid_invoice: dict) -> None:
    mine = client.get(INVOICES_URL, headers=client_headers).get_json()
    others = client.get(INVOICES_URL, headers=other_client_headers).get_json()

    assert mine["meta"]["total"] == 1
    assert others["meta"]["total"] == 0


def test_return_on_a_cached_invoice_shows_it_returned(client: FlaskClient, client_headers: dict, admin_headers: dict, paid_invoice: dict) -> None:
    url = f"{INVOICES_URL}/{paid_invoice['invoice_number']}"
    assert client.get(url, headers=client_headers).get_json()["data"]["status"] == "paid"  # Now it's cached
    body = {"reason": "Damaged packaging", "lines": [{"invoice_line_id": paid_invoice["invoice_lines"][0]["id"], "quantity": "2"}]}
    client.post(f"{url}/returns", json=body, headers=admin_headers)

    assert client.get(url, headers=client_headers).get_json()["data"]["status"] == "returned"