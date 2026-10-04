"""Application middlewares and their registration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.middlewares.request_logging import RequestLoggingMiddleware

__all__ = ["RequestLoggingMiddleware", "register_middlewares"]


def register_middlewares(app: FastAPI) -> None:
    """Attach all middlewares. Added last = outermost, so request logging wraps CORS."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )
    app.add_middleware(RequestLoggingMiddleware)
