"""Organization and organization-scoped membership contracts."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator

from app.core.enums import MembershipRole, MembershipStatus, TenantStatus
from app.schemas.base import ORMResponse, RequestSchema


class TenantCreateRequest(RequestSchema):
    name: str = Field(min_length=1, pattern=r"\S")
    slug: str = Field(pattern=r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")

    @field_validator("slug")
    @classmethod
    def validate_reserved_slug(cls, value: str) -> str:
        if value in {"admin", "api", "www", "auth"}:
            raise ValueError("This slug is reserved for SmartHire")
        return value


class TenantUpdateRequest(RequestSchema):
    name: str = Field(min_length=1, pattern=r"\S")


class TenantResponse(ORMResponse):
    id: UUID
    name: str
    slug: str
    status: TenantStatus
    created_at: datetime
    updated_at: datetime


class MembershipResponse(ORMResponse):
    id: UUID
    tenant_id: UUID
    user_id: UUID
    role: MembershipRole
    status: MembershipStatus
    created_at: datetime
    updated_at: datetime


class UserMembershipResponse(MembershipResponse):
    tenant: TenantResponse


class MembershipUpdateRequest(RequestSchema):
    role: MembershipRole | None = None
    status: MembershipStatus | None = None

    @model_validator(mode="after")
    def validate_changes(self) -> "MembershipUpdateRequest":
        if not self.model_fields_set:
            raise ValueError("Provide role or status")
        if any(getattr(self, field) is None for field in self.model_fields_set):
            raise ValueError("Provided fields cannot be null")
        return self


class TenantCreationResponse(BaseModel):
    organization: TenantResponse
    membership: MembershipResponse
