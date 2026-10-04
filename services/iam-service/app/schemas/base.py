"""Shared request settings, ORM parsing, response envelopes, and pagination."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=False)


class ORMResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SuccessResponse[T](BaseModel):
    success: Literal[True] = True
    data: T


class ErrorResponse(BaseModel):
    """Matches the existing AppError handler's response body."""

    error: str


class Page[T](BaseModel):
    items: list[T]
    total: int = Field(ge=0)
    offset: int = Field(ge=0)
    limit: int = Field(ge=1, le=100)
