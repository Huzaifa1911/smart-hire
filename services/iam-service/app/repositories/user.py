"""Global account lookups and membership-based organization listings."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select

from app.core.enums import MembershipStatus
from app.models.tenant_membership import TenantMembership
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(func.lower(func.btrim(User.email)) == func.lower(func.btrim(email)))
        )
        return result.scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        result = await self.session.execute(
            select(
                select(User.id)
                .where(func.lower(func.btrim(User.email)) == func.lower(func.btrim(email)))
                .exists()
            )
        )
        return bool(result.scalar_one())

    async def list_by_tenant(
        self,
        tenant_id: UUID,
        *,
        status: MembershipStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[User]:
        self.validate_pagination(limit, offset)
        statement = (
            select(User)
            .join(TenantMembership, TenantMembership.user_id == User.id)
            .where(TenantMembership.tenant_id == tenant_id)
        )
        if status is not None:
            statement = statement.where(TenantMembership.status == status)
        result = await self.session.execute(
            statement.order_by(User.created_at, User.id).limit(limit).offset(offset)
        )
        return result.scalars().all()
