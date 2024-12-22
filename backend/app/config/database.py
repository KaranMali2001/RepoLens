from app.config.config import settings
from sqlalchemy.orm import sessionmaker, declarative_base


from typing import AsyncGenerator

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False,
)
Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()
