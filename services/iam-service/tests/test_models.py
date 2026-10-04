"""Verify IAM mapping invariants and PostgreSQL migration SQL without a server."""

from io import StringIO
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from pydantic import TypeAdapter, ValidationError
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import configure_mappers

from app.core.enums import InvitationStatus
from app.models import Base, TenantInvitation, TenantMembership, User


def test_global_identity_and_organization_memberships():
    configure_mappers()
    assert set(Base.metadata.tables) == {
        "users",
        "tenants",
        "tenant_memberships",
        "tenant_invitations",
    }
    assert "tenant_id" not in User.__table__.columns
    assert "role" not in User.__table__.columns
    assert "is_candidate" in User.__table__.columns
    assert any(
        tuple(c.name for c in constraint.columns) == ("tenant_id", "user_id")
        for constraint in TenantMembership.__table__.constraints
    )


def test_inviter_must_belong_to_invited_organization():
    foreign_keys = TenantInvitation.__table__.foreign_key_constraints
    assert any(
        [(element.parent.name, element.target_fullname) for element in constraint.elements]
        == [
            ("tenant_id", "tenant_memberships.tenant_id"),
            ("invited_by_membership_id", "tenant_memberships.id"),
        ]
        for constraint in foreign_keys
    )


def test_migration_preserves_postgres_constraints():
    output = StringIO()
    config = Config(str(Path(__file__).parents[1] / "alembic.ini"), output_buffer=output)
    command.upgrade(config, "head", sql=True)
    sql = output.getvalue()
    assert "is_candidate BOOLEAN DEFAULT false NOT NULL" in sql
    assert "CREATE TYPE membership_role AS ENUM ('owner', 'recruiter')" in sql
    assert (
        "CREATE TYPE invitation_status AS ENUM ('pending', 'accepted', 'revoked', 'expired')" in sql
    )
    assert "ck_invitations_status" not in sql
    assert "lower(btrim(email))" in sql
    assert "WHERE status = 'pending'" in sql
    assert "FOREIGN KEY(tenant_id, invited_by_membership_id)" in sql
    assert "expires_at > created_at" in sql
    assert "accepted_by_user_id IS NOT NULL AND accepted_at IS NOT NULL" in sql


def test_shared_enum_validates_api_and_database_values():
    adapter = TypeAdapter(InvitationStatus)
    assert adapter.validate_python("pending") is InvitationStatus.PENDING
    assert adapter.dump_json(InvitationStatus.PENDING) == b'"pending"'
    with pytest.raises(ValidationError):
        adapter.validate_python("unknown")
    column_type = TenantInvitation.__table__.c.status.type
    dialect = postgresql.dialect()
    bind = column_type.bind_processor(dialect)
    result = column_type.result_processor(dialect, None)
    assert bind(InvitationStatus.PENDING) == "pending"
    assert result("accepted") is InvitationStatus.ACCEPTED
    with pytest.raises(LookupError):
        bind("unknown")


def test_initial_migration_drops_enum_types_after_tables():
    output = StringIO()
    config = Config(str(Path(__file__).parents[1] / "alembic.ini"), output_buffer=output)
    command.downgrade(config, "0001:base", sql=True)
    sql = output.getvalue()
    for name in (
        "invitation_status",
        "membership_status",
        "membership_role",
        "user_status",
        "tenant_status",
    ):
        assert f"DROP TYPE {name}" in sql
        assert sql.index("DROP TABLE tenants") < sql.index(f"DROP TYPE {name}")
