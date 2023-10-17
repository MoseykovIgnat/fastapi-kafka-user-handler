from functools import lru_cache

from loguru import logger
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaSettings(BaseSettings):
    host: str = Field(default="localhost")
    port: int = Field(default=29092)
    file_encoding: str = Field(default="utf-8")

    @property
    def instance(self) -> str:
        logger.info(f"Kafka instance: {self.host}:{self.port}")
        return f"{self.host}:{self.port}"

    model_config = SettingsConfigDict(
        extra="forbid",
        env_file=".env",
        env_prefix="kafka_",
    )


@lru_cache()
def get_kafka_settings() -> KafkaSettings:
    """Get application settings usually stored as environment variables.

    Returns:
        Settings: Application settings.
    """

    logger.info("Loading kafka config settings from the environment...")
    return KafkaSettings()
