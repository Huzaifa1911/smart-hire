"""Health/readiness endpoint handler."""

from app.core.database import ping_db
from app.core.settings import settings
from app.schemas.health import HealthCheck


async def get_health() -> HealthCheck:
    db_ok = await ping_db()
    return HealthCheck(
        status="UP" if db_ok else "DEGRADED",
        service=settings.service_name,
        database="up" if db_ok else "down",
    )
