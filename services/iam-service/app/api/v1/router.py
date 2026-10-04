"""Service router — central registration of all v1 routes."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, invitations, tenants, users
from app.api.v1.endpoints.health import get_health
from app.core.settings import settings
from app.schemas.auth import AuthResponse, OrganizationSignupResponse
from app.schemas.base import ErrorResponse, Page, SuccessResponse
from app.schemas.health import HealthCheck
from app.schemas.invitations import InvitationAcceptanceResponse, InvitationResponse
from app.schemas.tenants import (
    MembershipResponse,
    TenantCreationResponse,
    TenantResponse,
    UserMembershipResponse,
)
from app.schemas.users import UserResponse


def get_service_router() -> APIRouter:
    router = APIRouter(prefix=settings.base_path)
    router.get(
        "/health",
        summary="Health check",
        description="Check service and database health.",
        response_description="Returns UP/DEGRADED with HTTP Status Code 200 (OK).",
        status_code=200,
        response_model=HealthCheck,
    )(get_health)

    # Protected routes declare their intended authorization contract in descriptions.
    # Authentication dependencies will be added alongside actual authentication logic.
    pending = {501: {"model": ErrorResponse, "description": "Contract only; not implemented"}}
    router.post(
        "/auth/candidate-signup",
        tags=["Auth"],
        status_code=201,
        response_model=SuccessResponse[AuthResponse],
        responses=pending,
        description=(
            "Register a global account with candidate access; no candidate profile is created."
        ),
    )(auth.candidate_signup)
    router.post(
        "/auth/organization-signup",
        tags=["Auth"],
        status_code=201,
        response_model=SuccessResponse[OrganizationSignupResponse],
        responses=pending,
        description=(
            "Register a new account and organization with an owner membership "
            "atomically. Existing users create organizations through POST /tenants."
        ),
    )(auth.organization_signup)
    router.post(
        "/auth/login",
        tags=["Auth"],
        response_model=SuccessResponse[AuthResponse],
        responses=pending,
    )(auth.login)

    router.get(
        "/users/me",
        tags=["Users"],
        response_model=SuccessResponse[UserResponse],
        responses=pending,
        description="Authenticated: get the current account.",
    )(users.get_current_user)
    router.patch(
        "/users/me",
        tags=["Users"],
        response_model=SuccessResponse[UserResponse],
        responses=pending,
        description="Authenticated: update the current account's full name.",
    )(users.update_current_user)
    router.put(
        "/users/me/candidate-access",
        tags=["Users"],
        response_model=SuccessResponse[UserResponse],
        responses=pending,
        description=(
            "Authenticated: idempotently enable candidate access. Does not create a "
            "candidate profile."
        ),
    )(users.enable_candidate_access)
    router.get(
        "/users/me/memberships",
        tags=["Users"],
        response_model=SuccessResponse[Page[UserMembershipResponse]],
        responses=pending,
        description=(
            "Authenticated: list the current user's organization memberships, "
            "including their status."
        ),
    )(users.list_current_memberships)

    router.post(
        "/tenants",
        tags=["Organizations"],
        status_code=201,
        response_model=SuccessResponse[TenantCreationResponse],
        responses=pending,
        description=(
            "Authenticated: create an organization and owner membership for the "
            "current user atomically."
        ),
    )(tenants.create_tenant)
    router.get(
        "/tenants/{tenant_id}",
        tags=["Organizations"],
        response_model=SuccessResponse[TenantResponse],
        responses=pending,
        description="Active organization member: read organization details.",
    )(tenants.get_tenant)
    router.patch(
        "/tenants/{tenant_id}",
        tags=["Organizations"],
        response_model=SuccessResponse[TenantResponse],
        responses=pending,
        description=(
            "Organization owner: update the organization name. Slug and lifecycle "
            "changes are outside this contract."
        ),
    )(tenants.update_tenant)
    router.get(
        "/tenants/{tenant_id}/memberships",
        tags=["Memberships"],
        response_model=SuccessResponse[Page[MembershipResponse]],
        responses=pending,
        description="Organization owner: list memberships.",
    )(tenants.list_memberships)
    router.patch(
        "/tenants/{tenant_id}/memberships/{membership_id}",
        tags=["Memberships"],
        response_model=SuccessResponse[MembershipResponse],
        responses=pending,
        description=(
            "Organization owner: change membership role/status. Implementation must "
            "protect the last active owner."
        ),
    )(tenants.update_membership)
    router.post(
        "/tenants/{tenant_id}/invitations",
        tags=["Invitations"],
        status_code=201,
        response_model=SuccessResponse[InvitationResponse],
        responses=pending,
        description=(
            "Organization owner: invite an email address as a recruiter; invitation "
            "delivery is not implemented."
        ),
    )(tenants.create_invitation)
    router.get(
        "/tenants/{tenant_id}/invitations",
        tags=["Invitations"],
        response_model=SuccessResponse[Page[InvitationResponse]],
        responses=pending,
        description="Organization owner: list invitations.",
    )(tenants.list_invitations)
    router.post(
        "/tenants/{tenant_id}/invitations/{invitation_id}/revoke",
        tags=["Invitations"],
        response_model=SuccessResponse[InvitationResponse],
        responses=pending,
        description="Organization owner: revoke a pending invitation.",
    )(tenants.revoke_invitation)
    router.post(
        "/invitations/accept",
        tags=["Invitations"],
        response_model=SuccessResponse[InvitationAcceptanceResponse],
        responses=pending,
        description=(
            "Authenticated intended recipient: validate token, expiry and verified "
            "email, then accept and create/reactivate recruiter membership "
            "atomically."
        ),
    )(invitations.accept_invitation)
    return router
