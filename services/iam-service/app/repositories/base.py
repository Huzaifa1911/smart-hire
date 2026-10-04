"""Thin async data access. The service owns authorization and transactions."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base


class BaseRepository[ModelT: Base]:
    """Flush, never commit or roll back. Global CRUD is for trusted internal callers."""

    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def validate_pagination(limit: int, offset: int) -> None:
        if not 1 <= limit <= 100 or offset < 0:
            raise ValueError("limit must be between 1 and 100; offset must be nonnegative")

    async def get(self, id_: UUID, *, for_update: bool = False) -> ModelT | None:
        if not for_update:
            return await self.session.get(self.model, id_)
        # Always query for a lock, even if the object is already in the identity map.
        result = await self.session.execute(
            select(self.model)
            .where(self.model.id == id_)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        return result.scalar_one_or_none()

    async def list(self, *, limit: int = 100, offset: int = 0) -> Sequence[ModelT]:
        self.validate_pagination(limit, offset)
        result = await self.session.execute(
            select(self.model)
            .order_by(self.model.created_at, self.model.id)
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def add(self, obj: ModelT) -> ModelT:
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def save(self, obj: ModelT) -> ModelT:
        """Flush an existing session-managed object after the service changes fields."""
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: ModelT) -> None:
        await self.session.delete(obj)
        await self.session.flush()

    async def count(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(self.model))
        return int(result.scalar_one())
