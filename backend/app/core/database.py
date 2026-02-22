from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


def get_engine(database_url: str):
    """Create and return async engine. Called lazily to avoid import-time side effects."""
    return create_async_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
    )


def get_session_factory(engine):
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


# Module-level references (initialized on first use or via lifespan)
_engine = None
_session_factory = None


def init_db(database_url: str, echo: bool = False):
    """Initialize the engine and session factory. Call this from main.py lifespan."""
    global _engine, _session_factory
    _engine = create_async_engine(database_url, echo=echo, pool_pre_ping=True)
    _session_factory = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_db() -> AsyncSession:
    """FastAPI dependency: yields a database session per request."""
    if _session_factory is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    async with _session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
