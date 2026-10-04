"""FastAPI application factory: create_application(), lifespan, routers, middleware."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import get_service_router
from app.core.database import engine
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.core.settings import settings
from app.middlewares import register_middlewares


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    await engine.dispose()


def create_application() -> FastAPI:
    configure_logging()

    application = FastAPI(
        title="SmartHire Candidate Service",
        description="Candidate profiles, resumes, and skills foundation for SmartHire.",
        debug=settings.debug,
        lifespan=lifespan,
        docs_url=f"{settings.base_path}/swagger",
        redoc_url=f"{settings.base_path}/redoc",
        openapi_url=f"{settings.base_path}/openapi.json",
    )

    register_middlewares(application)
    application.include_router(get_service_router())
    register_exception_handlers(application)

    return application


app = create_application()
