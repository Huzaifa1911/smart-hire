"""IAM endpoint declarations; business logic is intentionally unimplemented."""

from uuid import UUID

from fastapi import Query

from app.core.exceptions import AppError
from app.schemas.invitations import InvitationCreateRequest
from app.schemas.tenants import MembershipUpdateRequest, TenantCreateRequest, TenantUpdateRequest


async def create_tenant(body: TenantCreateRequest):
    raise AppError("This endpoint is not implemented yet", status_code=501)


async def get_tenant(tenant_id: UUID):
    raise AppError("This endpoint is not implemented yet", status_code=501)


async def update_tenant(tenant_id: UUID, body: TenantUpdateRequest):
    raise AppError("This endpoint is not implemented yet", status_code=501)


async def list_memberships(
    tenant_id: UUID, offset: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)
):
    raise AppError("This endpoint is not implemented yet", status_code=501)


async def update_membership(tenant_id: UUID, membership_id: UUID, body: MembershipUpdateRequest):
    raise AppError("This endpoint is not implemented yet", status_code=501)


async def create_invitation(tenant_id: UUID, body: InvitationCreateRequest):
    raise AppError("This endpoint is not implemented yet", status_code=501)


async def list_invitations(
    tenant_id: UUID, offset: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)
):
    raise AppError("This endpoint is not implemented yet", status_code=501)


async def revoke_invitation(tenant_id: UUID, invitation_id: UUID):
    raise AppError("This endpoint is not implemented yet", status_code=501)
