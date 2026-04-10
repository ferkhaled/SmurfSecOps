from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_root_endpoint_returns_service_metadata() -> None:
    response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["service"] == "berryshop-api"
    assert payload["docs"] == "/docs"


def test_healthz_endpoint_reports_ok() -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_products_endpoint_returns_seed_data() -> None:
    response = client.get("/api/v1/products")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 3
    assert payload["items"][0]["name"] == "Smurfberry Jam"
