"""Global user contracts. Password hashes are never exposed."""

from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, Field

from app.core.enums import UserStatus
from app.schemas.base import ORMResponse, RequestSchema


class UserResponse(ORMResponse):
    id: UUID
    email: EmailStr
    full_name: str
    status: UserStatus
    is_candidate: bool
    created_at: datetime
    updated_at: datetime


class UserUpdateRequest(RequestSchema):
    full_name: str = Field(min_length=1, pattern=r"\S")
