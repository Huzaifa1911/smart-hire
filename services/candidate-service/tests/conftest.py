"""Pytest fixtures."""

import os

import pytest
from fastapi.testclient import TestClient

# Required config must exist before the app (and its settings) import.
os.environ.setdefault("CANDIDATE_DB_USER", "candidate")
os.environ.setdefault("CANDIDATE_DB_PASSWORD", "candidate")
os.environ.setdefault("CANDIDATE_DB_NAME", "candidate")


@pytest.fixture
def client() -> TestClient:
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
