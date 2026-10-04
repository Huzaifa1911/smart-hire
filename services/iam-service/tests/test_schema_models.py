"""Validate response contracts against actual IAM ORM objects."""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.core.enums import (
    InvitationStatus,
    MembershipRole,
    MembershipStatus,
    TenantStatus,
    UserStatus,
)
from app.models import Tenant, TenantInvitation, TenantMembership, User
from app.schemas.invitations import InvitationResponse
from app.schemas.tenants import TenantResponse, UserMembershipResponse
from app.schemas.users import UserResponse


def test_user_response_serializes_orm_enum_without_password_hash():
    now = datetime.now(UTC)
    user = User(
        id=uuid4(),
        email="alice@example.com",
        full_name="Alice",
        password_hash="private",
        status=UserStatus.ACTIVE,
        is_candidate=True,
        created_at=now,
        updated_at=now,
    )
    response = UserResponse.model_validate(user).model_dump(mode="json")
    assert response["status"] == "active"
    assert response["is_candidate"] is True
    assert "password_hash" not in response


def test_membership_response_includes_loaded_organization():
    now = datetime.now(UTC)
    tenant = Tenant(
        id=uuid4(),
        name="Acme",
        slug="acme",
        status=TenantStatus.ACTIVE,
        created_at=now,
        updated_at=now,
    )
    membership = TenantMembership(
        id=uuid4(),
        tenant_id=tenant.id,
        user_id=uuid4(),
        role=MembershipRole.OWNER,
        status=MembershipStatus.ACTIVE,
        created_at=now,
        updated_at=now,
        tenant=tenant,
    )
    response = UserMembershipResponse.model_validate(membership).model_dump(mode="json")
    assert response["role"] == "owner"
    assert response["tenant"] == TenantResponse.model_validate(tenant).model_dump(mode="json")


def test_invitation_response_excludes_hash_and_preserves_nullable_acceptance():
    now = datetime.now(UTC)
    invitation = TenantInvitation(
        id=uuid4(),
        tenant_id=uuid4(),
        email="bob@example.com",
        invited_by_membership_id=uuid4(),
        token_hash="private",
        status=InvitationStatus.PENDING,
        created_at=now,
        expires_at=now + timedelta(days=1),
        accepted_by_user_id=None,
        accepted_at=None,
    )
    response = InvitationResponse.model_validate(invitation).model_dump(mode="json")
    assert response["status"] == "pending"
    assert response["accepted_by_user_id"] is None
    assert response["accepted_at"] is None
    assert "token_hash" not in response
