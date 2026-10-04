"""Configuration validation and safe database connection construction."""

import pytest
from pydantic import ValidationError

from app.core.settings import DatabaseSettings, Settings


def test_candidate_environment_and_path_normalization(monkeypatch):
    monkeypatch.setenv("CANDIDATE_SERVICE_NAME", "custom-candidate")
    monkeypatch.setenv("CANDIDATE_DB_PORT", "5542")
    config = Settings(_env_file=None, base_path="candidate-service/v1")
    assert config.service_name == "custom-candidate"
    assert config.base_path == "/candidate-service/v1"
    assert config.database.port == 5542


@pytest.mark.parametrize("overrides", [{"log_level": "invalid"}, {"cors_allow_origins": []}])
def test_invalid_service_configuration(overrides):
    with pytest.raises(ValidationError):
        Settings(_env_file=None, **overrides)


def test_database_credentials_are_required(monkeypatch):
    for name in ("CANDIDATE_DB_USER", "CANDIDATE_DB_PASSWORD", "CANDIDATE_DB_NAME"):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(ValidationError):
        DatabaseSettings(_env_file=None)


def test_database_url_preserves_special_characters():
    config = DatabaseSettings(
        _env_file=None, user="candidate@local", password="p@ss:/?#", name="candidate"
    )
    assert config.url.username == "candidate@local"
    assert config.url.password == "p@ss:/?#"
    assert "p@ss" not in str(config.url)
