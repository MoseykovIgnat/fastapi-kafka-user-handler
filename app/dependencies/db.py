from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


from app.core.app_settings import get_app_settings

settings = get_app_settings()
engine = create_async_engine(
    f"{settings.DATABASE_URL}_pytest" if settings.TESTING else settings.DATABASE_URL,
    future=True,
    pool_pre_ping=True,
)


async_session = sessionmaker(  # noqa
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


class PaginationAndFiltersParams:
    def __init__(
        self,
        limit: int = 5,
        page: int = 1,
        email: str = "",
        name: str = "",
        surname: str = "",
    ):
        self.skip: int = (page - 1) * limit
        self.limit: int = limit
        self.name: str = name
        self.surname: str = surname
        self.email: str = email
