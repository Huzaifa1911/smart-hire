"""Authentication contracts, not authentication logic."""

from typing import Literal

from pydantic import BaseModel, EmailStr, Field, SecretStr

from app.schemas.base import RequestSchema
from app.schemas.tenants import (
    MembershipResponse,
    TenantCreateRequest,
    TenantResponse,
    UserMembershipResponse,
)
from app.schemas.users import UserResponse


class CandidateSignupRequest(RequestSchema):
    email: EmailStr
    password: SecretStr = Field(min_length=1)
    full_name: str = Field(min_length=1, pattern=r"\S")


class OrganizationSignupRequest(CandidateSignupRequest):
    organization: TenantCreateRequest


class LoginRequest(RequestSchema):
    email: EmailStr
    password: SecretStr = Field(min_length=1)


class TokenResponse(BaseModel):
    access_token: str = Field(min_length=1)
    token_type: Literal["bearer"] = "bearer"
    expires_in: int = Field(
        gt=0, description="Access-token lifetime in seconds; current policy is 900 (15 minutes)"
    )


class AuthResponse(TokenResponse):
    user: UserResponse
    memberships: list[UserMembershipResponse]


class OrganizationSignupResponse(AuthResponse):
    organization: TenantResponse
    membership: MembershipResponse
