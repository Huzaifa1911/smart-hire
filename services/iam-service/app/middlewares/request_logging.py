"""Request logging middleware: one line per HTTP request, level by status."""

import logging
import time
import uuid
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("app.request")


def _level_for(status_code: int) -> int:
    # Any non-success (4xx and 5xx) is logged at ERROR; 2xx/3xx at INFO.
    return logging.ERROR if status_code >= 400 else logging.INFO


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log method, path, status, duration; stamp X-Request-ID for correlation.

    Unhandled exceptions emit an ERROR access line before being re-raised for
    server error handling. Duration covers response creation, not body streaming.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = uuid.uuid4().hex[:12]
        request.state.request_id = request_id
        start = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000
            logger.error(
                "%s %s -> 500 (%.1fms) [%s]",
                request.method,
                request.url.path,
                duration_ms,
                request_id,
            )
            raise

        duration_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Request-ID"] = request_id
        logger.log(
            _level_for(response.status_code),
            "%s %s -> %s (%.1fms) [%s]",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            request_id,
        )
        return response
