from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from ToDo.src.core.exceptions.base import BaseError

DATABASE_URL = "sqlite+aiosqlite:///./app.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
)

async def get_session():
    try:
        async with async_session_maker() as session:
            yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def init_db():
    async with engine.begin() as conn:
        from src.infra.models.models import Base  
        await conn.run_sync(Base.metadata.create_all)
