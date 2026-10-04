"""Invitation data access; callers provide a hash, never the raw token."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select

from app.core.enums import InvitationStatus
from app.models.tenant_invitation import TenantInvitation
from app.repositories.base import BaseRepository


class TenantInvitationRepository(BaseRepository[TenantInvitation]):
    model = TenantInvitation

    async def get_for_tenant(
        self, tenant_id: UUID, invitation_id: UUID, *, for_update: bool = False
    ) -> TenantInvitation | None:
        statement = select(TenantInvitation).where(
            TenantInvitation.tenant_id == tenant_id, TenantInvitation.id == invitation_id
        )
        if for_update:
            statement = statement.with_for_update().execution_options(populate_existing=True)
        return (await self.session.execute(statement)).scalar_one_or_none()

    async def get_by_token_hash(
        self, token_hash: str, *, for_update: bool = False
    ) -> TenantInvitation | None:
        statement = select(TenantInvitation).where(TenantInvitation.token_hash == token_hash)
        if for_update:
            statement = statement.with_for_update().execution_options(populate_existing=True)
        return (await self.session.execute(statement)).scalar_one_or_none()

    async def get_pending_by_email(self, tenant_id: UUID, email: str) -> TenantInvitation | None:
        """Includes expired-but-still-pending rows, matching the uniqueness constraint."""
        statement = select(TenantInvitation).where(
            TenantInvitation.tenant_id == tenant_id,
            func.lower(func.btrim(TenantInvitation.email)) == func.lower(func.btrim(email)),
            TenantInvitation.status == InvitationStatus.PENDING,
        )
        return (await self.session.execute(statement)).scalar_one_or_none()

    async def list_by_tenant(
        self,
        tenant_id: UUID,
        *,
        status: InvitationStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[TenantInvitation]:
        self.validate_pagination(limit, offset)
        statement = select(TenantInvitation).where(TenantInvitation.tenant_id == tenant_id)
        if status is not None:
            statement = statement.where(TenantInvitation.status == status)
        return (
            (
                await self.session.execute(
                    statement.order_by(TenantInvitation.created_at, TenantInvitation.id)
                    .limit(limit)
                    .offset(offset)
                )
            )
            .scalars()
            .all()
        )

    async def count_by_tenant(
        self, tenant_id: UUID, *, status: InvitationStatus | None = None
    ) -> int:
        statement = (
            select(func.count())
            .select_from(TenantInvitation)
            .where(TenantInvitation.tenant_id == tenant_id)
        )
        if status is not None:
            statement = statement.where(TenantInvitation.status == status)
        return int((await self.session.execute(statement)).scalar_one())
