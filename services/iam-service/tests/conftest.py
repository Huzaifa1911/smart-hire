"""Pytest fixtures."""

import os

import pytest
from fastapi.testclient import TestClient

# Required config must exist before the app (and its settings) import.
os.environ.setdefault("IAM_DB_USER", "iam")
os.environ.setdefault("IAM_DB_PASSWORD", "iam")
os.environ.setdefault("IAM_DB_NAME", "iam")


@pytest.fixture
def client() -> TestClient:
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
