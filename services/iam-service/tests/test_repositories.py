"""Check transaction ownership and security-sensitive PostgreSQL query construction."""

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from sqlalchemy.dialects import postgresql

from app.core.enums import InvitationStatus, MembershipStatus
from app.models import User
from app.repositories import (
    TenantInvitationRepository,
    TenantMembershipRepository,
    UserRepository,
)


@pytest.fixture
def session():
    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    result.scalar_one.return_value = 0
    result.scalars.return_value.all.return_value = []
    mocked = MagicMock()
    mocked.execute = AsyncMock(return_value=result)
    mocked.get = AsyncMock(return_value=None)
    mocked.flush = AsyncMock()
    mocked.refresh = AsyncMock()
    mocked.delete = AsyncMock()
    mocked.commit = AsyncMock()
    mocked.rollback = AsyncMock()
    return mocked


def compiled_query(session):
    statement = session.execute.call_args.args[0]
    compiled = statement.compile(dialect=postgresql.dialect())
    return str(compiled), compiled.params


async def test_mutations_flush_without_owning_transaction(session):
    repository = UserRepository(session)
    user = User(email="alice@example.com", password_hash="hashed", full_name="Alice")
    assert await repository.add(user) is user
    session.add.assert_called_once_with(user)
    await repository.save(user)
    await repository.delete(user)
    assert session.flush.await_count == 3
    assert session.refresh.await_count == 2
    session.commit.assert_not_awaited()
    session.rollback.assert_not_awaited()


async def test_email_lookup_matches_normalized_unique_index(session):
    await UserRepository(session).get_by_email(" Alice@example.com ")
    sql, params = compiled_query(session)
    assert "lower(btrim(users.email)) = lower(btrim(" in sql
    assert " Alice@example.com " in params.values()


async def test_membership_lookup_scopes_and_locks(session):
    tenant_id, membership_id = uuid4(), uuid4()
    await TenantMembershipRepository(session).get_for_tenant(
        tenant_id, membership_id, for_update=True
    )
    sql, params = compiled_query(session)
    assert "tenant_memberships.tenant_id =" in sql
    assert "tenant_memberships.id =" in sql
    assert {tenant_id, membership_id}.issubset(set(params.values()))
    assert "FOR UPDATE" in sql
    assert session.execute.call_args.args[0].get_execution_options()["populate_existing"]


async def test_invitation_lookup_scopes_and_locks(session):
    tenant_id, invitation_id = uuid4(), uuid4()
    await TenantInvitationRepository(session).get_for_tenant(
        tenant_id, invitation_id, for_update=True
    )
    sql, params = compiled_query(session)
    assert "tenant_invitations.tenant_id =" in sql
    assert "tenant_invitations.id =" in sql
    assert {tenant_id, invitation_id}.issubset(set(params.values()))
    assert "FOR UPDATE" in sql


async def test_expired_pending_invitation_is_not_hidden(session):
    tenant_id = uuid4()
    await TenantInvitationRepository(session).get_pending_by_email(tenant_id, "alice@example.com")
    sql, params = compiled_query(session)
    assert "tenant_invitations.status =" in sql
    assert InvitationStatus.PENDING in params.values()
    assert "expires_at" not in sql.split("WHERE")[1]


async def test_membership_list_and_count_use_same_scope(session):
    repository = TenantMembershipRepository(session)
    tenant_id = uuid4()
    await repository.list_by_tenant(tenant_id, status=MembershipStatus.ACTIVE, limit=20, offset=10)
    sql, params = compiled_query(session)
    assert "ORDER BY tenant_memberships.created_at, tenant_memberships.id" in sql
    assert tenant_id in params.values() and MembershipStatus.ACTIVE in params.values()
    await repository.count_by_tenant(tenant_id, status=MembershipStatus.ACTIVE)
    count_sql, count_params = compiled_query(session)
    assert "tenant_memberships.tenant_id =" in count_sql
    assert "tenant_memberships.status =" in count_sql
    assert tenant_id in count_params.values() and MembershipStatus.ACTIVE in count_params.values()


async def test_user_memberships_eagerly_load_organization(session):
    await TenantMembershipRepository(session).list_by_user(uuid4())
    statement = session.execute.call_args.args[0]
    assert statement._with_options  # Includes selectinload for ORM response serialization.


async def test_repository_rejects_unbounded_pagination(session):
    for limit, offset in [(0, 0), (101, 0), (20, -1)]:
        with pytest.raises(ValueError):
            await UserRepository(session).list(limit=limit, offset=offset)
    session.execute.assert_not_awaited()
