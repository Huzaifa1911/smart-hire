"""Service identity and dependency health contracts without live PostgreSQL."""

import pytest

from app.api.v1.endpoints import health


@pytest.mark.parametrize(
    ("database_ok", "expected_status", "expected_database"),
    [(True, "UP", "up"), (False, "DEGRADED", "down")],
)
def test_health(client, monkeypatch, database_ok, expected_status, expected_database):
    async def ping():
        return database_ok

    monkeypatch.setattr(health, "ping_db", ping)
    response = client.get("/candidate-service/v1/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": expected_status,
        "service": "candidate-service",
        "database": expected_database,
    }


def test_openapi_uses_candidate_routes(client):
    response = client.get("/candidate-service/v1/openapi.json")
    assert response.status_code == 200
    document = response.json()
    assert document["info"]["title"] == "SmartHire Candidate Service"
    assert "/candidate-service/v1/health" in document["paths"]
    assert all(path.startswith("/candidate-service/v1/") for path in document["paths"])
    assert client.get("/candidate-service/v1/swagger").status_code == 200
    assert client.get("/candidate-service/v1/redoc").status_code == 200
