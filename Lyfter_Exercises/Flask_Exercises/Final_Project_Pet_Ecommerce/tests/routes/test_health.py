from http import HTTPStatus

from flask.testing import FlaskClient

def test_health_with_database_and_cache_up_returns_200(client: FlaskClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {"status": "ok", "database": "ok", "cache": "ok"}