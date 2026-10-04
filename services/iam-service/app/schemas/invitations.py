"""Invitation contracts; token hashes stay private."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, SecretStr

from app.core.enums import InvitationStatus
from app.schemas.base import ORMResponse, RequestSchema
from app.schemas.tenants import MembershipResponse


class InvitationCreateRequest(RequestSchema):
    email: EmailStr


class InvitationAcceptRequest(RequestSchema):
    token: SecretStr = Field(min_length=1)


class InvitationResponse(ORMResponse):
    id: UUID
    tenant_id: UUID
    email: EmailStr
    invited_by_membership_id: UUID
    status: InvitationStatus
    expires_at: datetime
    accepted_by_user_id: UUID | None
    accepted_at: datetime | None
    created_at: datetime


class InvitationAcceptanceResponse(BaseModel):
    invitation: InvitationResponse
    membership: MembershipResponse
