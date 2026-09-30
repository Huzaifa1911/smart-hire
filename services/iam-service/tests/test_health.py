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
    response = client.get("/iam-service/v1/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": expected_status,
        "service": "iam-service",
        "database": expected_database,
    }


def test_openapi_uses_iam_routes(client):
    response = client.get("/iam-service/v1/openapi.json")
    assert response.status_code == 200
    document = response.json()
    assert document["info"]["title"] == "SmartHire IAM Service"
    assert set(document["paths"]) == {"/iam-service/v1/health"}
    assert client.get("/iam-service/v1/swagger").status_code == 200
    assert client.get("/iam-service/v1/redoc").status_code == 200
