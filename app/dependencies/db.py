from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import async_session


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
