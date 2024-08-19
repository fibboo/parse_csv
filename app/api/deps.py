from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import SessionLocal


async def get_db() -> AsyncSession:
    session = SessionLocal()

    try:
        yield session

    finally:
        await session.commit()
        await session.close()
