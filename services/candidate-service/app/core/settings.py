"""Candidate settings — grouped and validated (env_prefix CANDIDATE_)."""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


# --------------------------------------------------------------------------- #
# Database
# --------------------------------------------------------------------------- #
class DatabaseSettings(BaseSettings):
    """PostgreSQL connection + pool settings (env_prefix CANDIDATE_DB_)."""

    model_config = SettingsConfigDict(
        env_prefix="CANDIDATE_DB_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = Field(default="localhost", min_length=1)
    port: int = Field(default=5433, ge=1, le=65535)
    user: str = Field(min_length=1)
    password: str = Field(min_length=1)
    name: str = Field(min_length=1)

    pool_size: int = Field(default=10, ge=1)
    max_overflow: int = Field(default=0, ge=0)
    pool_recycle: int = Field(default=300, ge=0)
    pool_pre_ping: bool = True
    echo: bool = False

    @property
    def url(self) -> URL:
        return URL.create(
            "postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        )


# --------------------------------------------------------------------------- #
# Service
# --------------------------------------------------------------------------- #
class Settings(BaseSettings):
    """Top-level service settings (env_prefix CANDIDATE_)."""

    model_config = SettingsConfigDict(
        env_prefix="CANDIDATE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Service identity
    service_name: str = Field(default="candidate-service", min_length=1)
    debug: bool = False
    base_path: str = "/candidate-service/v1"

    # HTTP
    cors_allow_origins: list[str] = ["*"]

    # Logging
    log_level: str = "INFO"
    log_colors: bool = True

    # Grouped sub-settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)

    @field_validator("base_path")
    @classmethod
    def _normalize_path(cls, value: str) -> str:
        return "/" + value.strip("/")

    @field_validator("log_level")
    @classmethod
    def _validate_log_level(cls, value: str) -> str:
        level = value.upper()
        if level not in _LOG_LEVELS:
            raise ValueError(f"log_level must be one of {sorted(_LOG_LEVELS)}")
        return level

    @field_validator("cors_allow_origins")
    @classmethod
    def _non_empty_origins(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("cors_allow_origins must not be empty")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
