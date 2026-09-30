"""Health check schema."""

from pydantic import BaseModel


class HealthCheck(BaseModel):
    status: str
    service: str
    database: str
