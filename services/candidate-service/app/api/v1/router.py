"""Central registration of candidate-service v1 routes."""

from fastapi import APIRouter

from app.api.v1.endpoints.health import get_health
from app.core.settings import settings
from app.schemas.health import HealthCheck


def get_service_router() -> APIRouter:
    router = APIRouter(prefix=settings.base_path)
    router.get(
        "/health",
        summary="Health check",
        description="Check service and database health.",
        response_description="Returns UP/DEGRADED with HTTP Status Code 200 (OK).",
        status_code=200,
        response_model=HealthCheck,
    )(get_health)
    return router
