"""Standard success / error response envelopes."""

from typing import Any

from pydantic import BaseModel


class SuccessResponse[T](BaseModel):
    success: bool = True
    data: T


class ErrorResponse(BaseModel):
    success: bool = False
    status_code: int
    message: str
    details: list[dict[str, Any]] | None = None
