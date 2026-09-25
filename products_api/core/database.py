from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from products_api.core.settings import settings

engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
