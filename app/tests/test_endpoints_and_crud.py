import datetime

import pytest
import pytest_asyncio
import pytz
from httpx import AsyncClient
from loguru import logger
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import UsersCRUD
from app.dependencies.db import PaginationAndFiltersParams
from app.schemas.general import ResponseStatuses
from app.schemas.user import User, UserWithoutValidation
from app.models.user import User as UserModel


@pytest_asyncio.fixture(autouse=True, scope="function")
async def clear_user_table(async_db_session: AsyncSession):
    await async_db_session.execute(delete(UserModel))
    await async_db_session.commit()
    logger.success("Clear table users")


@pytest.mark.asyncio()
async def test_healthz(fake_session: AsyncClient):
    response = await fake_session.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": ResponseStatuses.ok}


dt_of_addition = datetime.datetime.now().astimezone(pytz.UTC).replace(tzinfo=None)


@pytest.mark.parametrize(
    "users_data_to_add_and_check",
    [
        (
            [
                User(
                    name="Петя",
                    surname="петров",
                    email="t1est@example.com",
                    birthday=dt_of_addition,
                ),
                User(
                    name="Вася",
                    surname="Васечкин",
                    email="vasya@example.com",
                    birthday=dt_of_addition,
                ),
            ]
        ),
    ],
    ids=["Check row"],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("clear_user_table")
async def test_addition_and_get_of_users_crud(
    users_data_to_add_and_check: list[User],
    async_db_session: AsyncSession,
):
    for user_data_to_add_and_check in users_data_to_add_and_check:
        await UsersCRUD.create_user(
            async_session=async_db_session,
            user_info=user_data_to_add_and_check,
        )
    rows = await UsersCRUD.get_users_with_pagination_and_filters(
        async_session=async_db_session,
        pagination_and_filters_params=PaginationAndFiltersParams(),
    )
    assert users_data_to_add_and_check == [
        User.model_validate(row.__dict__) for row in rows
    ]


@pytest.mark.parametrize(
    ("user_data_to_add_and_check", "new_user_data", "result_user"),
    [
        (
            User(
                name="Гриша",
                surname="Афанасьев",
                email="t1est@example.com",
                birthday=dt_of_addition,
            ),
            UserWithoutValidation(name="Петя"),
            User(
                name="Петя",
                surname="Афанасьев",
                email="t1est@example.com",
                birthday=dt_of_addition,
            ),
        ),
        (
            User(
                name="Гриша",
                surname="Афанасьев",
                email="t1est@example.com",
                birthday=dt_of_addition,
            ),
            UserWithoutValidation(surname="Кривцов"),
            User(
                name="Гриша",
                surname="Кривцов",
                email="t1est@example.com",
                birthday=dt_of_addition,
            ),
        ),
        (
            User(
                name="Гриша",
                surname="Кривцов",
                email="t1est@example.com",
                birthday=dt_of_addition,
            ),
            UserWithoutValidation(email="lol@lol.ru"),
            User(
                name="Гриша",
                surname="Кривцов",
                email="lol@lol.ru",
                birthday=dt_of_addition,
            ),
        ),
        (
            User(
                name="Гриша",
                surname="Кривцов",
                email="lol@lol.ru",
                birthday=dt_of_addition,
            ),
            UserWithoutValidation(birthday=dt_of_addition - datetime.timedelta(days=1)),
            User(
                name="Гриша",
                surname="Кривцов",
                email="lol@lol.ru",
                birthday=dt_of_addition - datetime.timedelta(days=1),
            ),
        ),
    ],
    ids=["Patch user name", "Patch user surname", "Patch email", "Patch birthday"],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("clear_user_table")
async def test_addition_and_patch_users_crud(
    user_data_to_add_and_check: User,
    new_user_data: UserWithoutValidation,
    result_user: User,
    async_db_session: AsyncSession,
):
    created_user = await UsersCRUD.create_user(
        async_session=async_db_session,
        user_info=user_data_to_add_and_check,
    )

    await UsersCRUD.update_user(
        async_session=async_db_session,
        new_user_data=new_user_data,
        current_user=created_user,
        user_id=created_user.user_id,
    )

    rows = await UsersCRUD.get_users_with_pagination_and_filters(
        async_session=async_db_session,
        pagination_and_filters_params=PaginationAndFiltersParams(),
    )
    assert result_user == User.model_validate(rows[0].__dict__)


@pytest.mark.parametrize(
    (
        "input_json",
        "create_status_code",
        "result_of_creating",
        "delete_status_code",
        "amount_of_rows",
    ),
    [
        (
            {
                "Name": "mosey",
                "Surname": "moseyka",
                "Email": "moseyka@example.com",
                "Birthday": "2023-10-17T01:12:15.566Z",
            },
            201,
            {
                "birthday": datetime.datetime(2023, 10, 17, 1, 12, 15, 566000),
                "email": "moseyka@example.com",
                "name": "mosey",
                "surname": "moseyka",
            },
            200,
            0,
        ),
    ],
    ids=["Patch user name"],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("clear_user_table")
async def test_delete_endpoint_email_duplicate_checker(
    input_json: dict[str, str],
    create_status_code: int,
    result_of_creating: dict[str, str | dict[str, str]],
    delete_status_code: int,
    amount_of_rows: int,
    fake_session: AsyncClient,
):
    response_create = await fake_session.post("/users", json=input_json)
    assert response_create.status_code == create_status_code
    assert (
        User.model_validate(response_create.json().get("user")).model_dump(
            exclude_none=True,
        )
        == result_of_creating
    )
    user_id = response_create.json().get("user").get("user_id")
    response_delete = await fake_session.delete(f"/users/{user_id}")
    assert response_delete.status_code == delete_status_code
    assert amount_of_rows == (await fake_session.get("/users")).json().get("length")
