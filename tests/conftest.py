import pytest_asyncio

from products_api.core.database import engine
from products_api.models import Base


@pytest_asyncio.fixture(autouse=True)
async def database_schema():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
