"""
KhaoGPT Database — SQLAlchemy async setup with SQLite for MVP
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import DATABASE_URL

# Disable prepared statement cache for PgBouncer/Supabase pooler compatibility
_connect_args = {}
if DATABASE_URL.startswith("postgresql"):
    _connect_args = {"statement_cache_size": 0}

engine = create_async_engine(DATABASE_URL, echo=False, connect_args=_connect_args)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    # Only run heavy schema generation on local dev or explicit seeding
    if os.getenv("VERCEL"):
        return
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
