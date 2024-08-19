import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.models.base import Base


@pytest_asyncio.fixture
async def engine(postgresql):
    connection = f'postgresql+asyncpg://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}'
    engine = create_async_engine(connection)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine


@pytest_asyncio.fixture
async def db_fixture(engine):
    SessionLocalPytest = async_sessionmaker(engine, autocommit=False, autoflush=False, expire_on_commit=False)
    session = SessionLocalPytest()

    yield session

    await session.close()


@pytest_asyncio.fixture
async def db_fixture2(engine):
    SessionLocalPytest = async_sessionmaker(engine, autocommit=False, autoflush=False, expire_on_commit=False)
    session = SessionLocalPytest()

    yield session

    await session.close()
