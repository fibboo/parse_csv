from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.configs.settings import settings

engine = create_async_engine(settings.database_url,
                             # echo=True  # When True, enable log output for every query
                             )

SessionLocal = async_sessionmaker(engine, autocommit=False, autoflush=False, expire_on_commit=False)
