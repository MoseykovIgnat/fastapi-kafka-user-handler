from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class AppSettings(BaseSettings):
    ENVIRONMENT: str = "test"
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/user_service"
    )
    app_name: str = "Awesome API"

    model_config = SettingsConfigDict(env_file=".env")


app_settings = AppSettings()

engine = create_async_engine(
    app_settings.DATABASE_URL,
    future=True,
    pool_pre_ping=True,
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
