from functools import lru_cache

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    TESTING: bool = False
    ENVIRONMENT: str = "test"
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/user_service"
    )

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_app_settings() -> AppSettings:
    """Get application settings usually stored as environment variables.

    Returns:
        Settings: Application settings.
    """

    logger.info("Loading FastAPI config settings from the environment...")
    return AppSettings()
