from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from core.config import app_setting

engine = create_async_engine(url=app_setting.database_dsn.unicode_string(), echo=True, future=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=True)

async def get_session():
    async with async_session() as session:
        yield session