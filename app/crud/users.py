from typing import Any, Sequence

from pydantic import EmailStr
from sqlalchemy import Row, RowMapping, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import PaginationAndFiltersParams
from app.models.user import User as UserModel
from app.schemas.user import User as UserSchema, UserWithoutValidation


class UsersCRUD:
    @staticmethod
    async def get_user_by_email(
        async_session: AsyncSession,
        email: EmailStr,
    ) -> None | UserModel:
        try:
            return (
                await async_session.execute(
                    select(UserModel).filter(UserModel.email == email),
                )
            ).scalar_one()
        except NoResultFound:
            return None

    @staticmethod
    async def get_user_by_id(
        async_session: AsyncSession,
        user_id: int,
    ) -> None | UserModel:
        try:
            return (
                await async_session.execute(
                    select(UserModel).filter(UserModel.user_id == user_id),
                )
            ).scalar_one()
        except NoResultFound:
            return None

    @staticmethod
    async def create_user(
        async_session: AsyncSession,
        user_info: UserSchema,
    ) -> UserModel:
        user_model_record = UserModel(**user_info.model_dump())
        async_session.add(user_model_record)
        await async_session.commit()
        await async_session.refresh(user_model_record)
        return user_model_record

    @staticmethod
    async def get_users_with_pagination_and_filters(
        async_session: AsyncSession,
        pagination_and_filters_params: PaginationAndFiltersParams,
    ) -> Sequence[Row | RowMapping | Any]:
        return (
            (
                await async_session.execute(
                    select(UserModel)
                    .filter(
                        UserModel.name.ilike(pagination_and_filters_params.name)
                        if pagination_and_filters_params.name
                        else True,
                        UserModel.surname.ilike(pagination_and_filters_params.surname)
                        if pagination_and_filters_params.surname
                        else True,
                        UserModel.email.ilike(pagination_and_filters_params.email)
                        if pagination_and_filters_params.email
                        else True,
                    )
                    .limit(pagination_and_filters_params.limit)
                    .offset(pagination_and_filters_params.skip),
                )
            )
            .scalars()
            .all()
        )

    @staticmethod
    async def update_user(
        async_session: AsyncSession,
        new_user_data: UserWithoutValidation,
        current_user: UserModel,
        user_id: int,
    ) -> UserModel:
        await async_session.execute(
            update(UserModel)
            .filter(UserModel.user_id == user_id)
            .values(**new_user_data.model_dump(exclude_none=True)),
        )
        await async_session.commit()
        await async_session.refresh(current_user)
        return current_user

    @staticmethod
    async def delete_user(
        async_session: AsyncSession,
        user: UserModel,
    ) -> UserModel:
        await async_session.delete(user)
        await async_session.commit()
        return user
