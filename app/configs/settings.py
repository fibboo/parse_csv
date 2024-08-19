from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = 'postgresql+asyncpg://user:password@localhost:5432/parse_csv'


settings = Settings()
