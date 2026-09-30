"""Configuration validation and safe database connection construction."""

import pytest
from pydantic import ValidationError

from app.core.settings import DatabaseSettings, Settings


def test_iam_environment_and_path_normalization(monkeypatch):
    monkeypatch.setenv("IAM_SERVICE_NAME", "custom-iam")
    monkeypatch.setenv("IAM_DB_PORT", "5542")
    config = Settings(_env_file=None, base_path="iam-service/v1")
    assert config.service_name == "custom-iam"
    assert config.base_path == "/iam-service/v1"
    assert config.database.port == 5542


@pytest.mark.parametrize("overrides", [{"log_level": "invalid"}, {"cors_allow_origins": []}])
def test_invalid_service_configuration(overrides):
    with pytest.raises(ValidationError):
        Settings(_env_file=None, **overrides)


def test_database_credentials_are_required(monkeypatch):
    for name in ("IAM_DB_USER", "IAM_DB_PASSWORD", "IAM_DB_NAME"):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(ValidationError):
        DatabaseSettings(_env_file=None)


def test_database_url_preserves_special_characters():
    config = DatabaseSettings(_env_file=None, user="iam@local", password="p@ss:/?#", name="iam")
    assert config.url.username == "iam@local"
    assert config.url.password == "p@ss:/?#"
    assert "p@ss" not in str(config.url)
