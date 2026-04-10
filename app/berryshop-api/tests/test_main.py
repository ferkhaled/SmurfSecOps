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


def test_search_endpoint_returns_matching_products() -> None:
    response = client.get("/api/v1/search?q=Smurfberry")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 1
    assert payload["items"][0]["name"] == "Smurfberry Jam"


def test_search_endpoint_returns_empty_for_no_match() -> None:
    response = client.get("/api/v1/search?q=gargamel")

    assert response.status_code == 200
    assert response.json()["count"] == 0


def test_debug_endpoint_disabled_by_default() -> None:
    response = client.get("/api/v1/debug")

    assert response.status_code == 200
    assert response.json()["debug"] is False


def test_debug_endpoint_enabled_with_env_var(monkeypatch) -> None:
    monkeypatch.setenv("DEBUG_MODE", "true")
    response = client.get("/api/v1/debug")

    assert response.status_code == 200
    assert response.json()["debug"] is True


def test_random_pick_returns_a_product() -> None:
    response = client.get("/api/v1/random-pick")

    assert response.status_code == 200
    payload = response.json()
    assert "picked" in payload
    assert "name" in payload["picked"]
