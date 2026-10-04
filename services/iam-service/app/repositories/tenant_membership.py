"""Tenant-scoped membership lookups and listings for workspace discovery."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.core.enums import MembershipStatus
from app.models.tenant_membership import TenantMembership
from app.repositories.base import BaseRepository


class TenantMembershipRepository(BaseRepository[TenantMembership]):
    model = TenantMembership

    async def get_for_tenant(
        self, tenant_id: UUID, membership_id: UUID, *, for_update: bool = False
    ) -> TenantMembership | None:
        statement = select(TenantMembership).where(
            TenantMembership.tenant_id == tenant_id, TenantMembership.id == membership_id
        )
        if for_update:
            statement = statement.with_for_update().execution_options(populate_existing=True)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_user(
        self, tenant_id: UUID, user_id: UUID, *, for_update: bool = False
    ) -> TenantMembership | None:
        statement = select(TenantMembership).where(
            TenantMembership.tenant_id == tenant_id, TenantMembership.user_id == user_id
        )
        if for_update:
            statement = statement.with_for_update().execution_options(populate_existing=True)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: UUID,
        *,
        status: MembershipStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[TenantMembership]:
        self.validate_pagination(limit, offset)
        statement = select(TenantMembership).where(TenantMembership.user_id == user_id)
        if status is not None:
            statement = statement.where(TenantMembership.status == status)
        # UserMembershipResponse includes organization details; avoid async lazy loading.
        statement = statement.options(selectinload(TenantMembership.tenant))
        result = await self.session.execute(
            statement.order_by(TenantMembership.created_at, TenantMembership.id)
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def count_by_user(self, user_id: UUID, *, status: MembershipStatus | None = None) -> int:
        statement = (
            select(func.count())
            .select_from(TenantMembership)
            .where(TenantMembership.user_id == user_id)
        )
        if status is not None:
            statement = statement.where(TenantMembership.status == status)
        return int((await self.session.execute(statement)).scalar_one())

    async def list_by_tenant(
        self,
        tenant_id: UUID,
        *,
        status: MembershipStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[TenantMembership]:
        self.validate_pagination(limit, offset)
        statement = select(TenantMembership).where(TenantMembership.tenant_id == tenant_id)
        if status is not None:
            statement = statement.where(TenantMembership.status == status)
        result = await self.session.execute(
            statement.order_by(TenantMembership.created_at, TenantMembership.id)
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def count_by_tenant(
        self, tenant_id: UUID, *, status: MembershipStatus | None = None
    ) -> int:
        statement = (
            select(func.count())
            .select_from(TenantMembership)
            .where(TenantMembership.tenant_id == tenant_id)
        )
        if status is not None:
            statement = statement.where(TenantMembership.status == status)
        return int((await self.session.execute(statement)).scalar_one())
