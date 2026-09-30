"""Async SQLAlchemy engine, session factory, Base, and get_db dependency."""

import logging
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.settings import settings

logger = logging.getLogger(__name__)

_db = settings.database


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


engine = create_async_engine(
    _db.url,
    echo=_db.echo,
    pool_size=_db.pool_size,
    max_overflow=_db.max_overflow,
    pool_recycle=_db.pool_recycle,
    pool_pre_ping=_db.pool_pre_ping,
)

SessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding an async session."""
    async with SessionFactory() as session:
        yield session


async def ping_db() -> bool:
    """Return True if the database answers a trivial query."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.warning("Database ping failed (%s)", type(exc).__name__)
        return False
