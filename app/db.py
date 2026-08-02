"""Async SQLAlchemy engine/session plumbing."""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

settings = get_settings()

_engine_kwargs = {"echo": False, "future": True}
# SQLite needs this to allow the connection to be shared across the async
# event loop correctly; Postgres (asyncpg) ignores it.
if settings.normalized_database_url.startswith("sqlite"):
    _engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    _engine_kwargs["pool_pre_ping"] = True

engine = create_async_engine(settings.normalized_database_url, **_engine_kwargs)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_models() -> None:
    """Create tables if they don't exist. Adequate for a single-tenant app;
    swap for Alembic migrations if the schema needs to evolve under live data."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
