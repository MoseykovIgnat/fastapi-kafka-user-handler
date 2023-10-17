import asyncio
import os

import pytest
import pytest_asyncio
from httpx import AsyncClient
from loguru import logger
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy_utils import create_database, drop_database
from sqlalchemy.engine import Connection

from app.core.app_settings import get_app_settings

os.environ["TESTING"] = "True"


@pytest.fixture(scope="session", autouse=True)
def _setup_db() -> None:
    database_url = f'{get_app_settings().DATABASE_URL.replace("postgresql+asyncpg", "postgresql")}_pytest'
    try:
        logger.info(get_app_settings())
        create_database(database_url)
        logger.info("Test database was created")
        base_dir = os.getcwd()
        alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
        command.upgrade(alembic_cfg, "head")
        logger.success(f"Success created test database. URL: {database_url}")
        yield
    except Exception as e:
        logger.warning(f"Failed to setup test database. Error: {e}")
        pytest.skip(
            "****** DB Setup failed, skipping test suit *******",
            allow_module_level=True,
        )
    finally:
        try:
            drop_database(database_url)
            logger.success("Success dropped test DB")
        except Exception as e:
            logger.warning(f"Got an error while deleting test DB. Error: {e}")


@pytest_asyncio.fixture(scope="session")
async def async_db_session(_setup_db, event_loop) -> Connection:
    from sqlalchemy.orm import sessionmaker

    try:
        engine = create_async_engine(f"{get_app_settings().DATABASE_URL}_pytest")
        async_session = sessionmaker(  # noqa
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        async with async_session() as session:
            yield session
    except Exception as e:
        logger.warning(
            f"Failed to create db_connection fixture on test DB"
            f" {f'{get_app_settings().DATABASE_URL}_pytest'}. Error: {e}",
        )
        pytest.skip(
            "****** DB connection fixture setup failed, skipping test suit *******",
            allow_module_level=True,
        )


@pytest_asyncio.fixture(scope="session")
async def fake_session():
    from app.main import app

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
