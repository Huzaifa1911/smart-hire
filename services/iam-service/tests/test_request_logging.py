"""Access logging, correlation, and unhandled exception behavior."""

import logging
import re

import pytest
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from app.middlewares.request_logging import RequestLoggingMiddleware


@pytest.mark.parametrize(
    ("status_code", "expected_level"),
    [(200, logging.INFO), (302, logging.INFO), (400, logging.ERROR), (503, logging.ERROR)],
)
def test_response_correlation_and_log_level(caplog, status_code, expected_level):
    application = FastAPI()
    application.add_middleware(RequestLoggingMiddleware)

    @application.get("/example")
    async def example(request: Request):
        return JSONResponse({"request_id": request.state.request_id}, status_code=status_code)

    with caplog.at_level(logging.INFO, logger="app.request"), TestClient(application) as client:
        response = client.get("/example?secret=private", follow_redirects=False)
        second_response = client.get("/example", follow_redirects=False)

    request_id = response.headers["X-Request-ID"]
    assert re.fullmatch(r"[0-9a-f]{12}", request_id)
    assert response.json()["request_id"] == request_id
    assert second_response.headers["X-Request-ID"] != request_id
    records = [record for record in caplog.records if record.name == "app.request"]
    assert len(records) == 2
    assert records[0].levelno == expected_level
    assert f"GET /example -> {status_code}" in records[0].getMessage()
    assert f"[{request_id}]" in records[0].getMessage()
    assert "secret" not in records[0].getMessage()


def test_unhandled_exception_is_logged_and_reraised(caplog):
    application = FastAPI()
    application.add_middleware(RequestLoggingMiddleware)

    @application.get("/failure")
    async def failure():
        raise RuntimeError("test failure")

    with (
        caplog.at_level(logging.INFO, logger="app.request"),
        TestClient(application) as client,
        pytest.raises(RuntimeError, match="test failure"),
    ):
        client.get("/failure")

    records = [record for record in caplog.records if record.name == "app.request"]
    assert len(records) == 1
    assert records[0].levelno == logging.ERROR
    assert "GET /failure -> 500" in records[0].getMessage()


def test_middleware_is_registered_in_iam(client):
    response = client.get("/iam-service/v1/openapi.json")
    assert re.fullmatch(r"[0-9a-f]{12}", response.headers["X-Request-ID"])
