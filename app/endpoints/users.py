from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import UsersCRUD
from app.dependencies.db import get_async_session, PaginationAndFiltersParams
from app.endpoints.settings import EndpointsTags
from app.schemas.general import ResponseStatuses
from app.schemas.user import (
    User as UserSchema,
    UserResponse,
    UsersGetResponse,
    UserWithoutValidation,
)

router = APIRouter(prefix="/users", tags=[EndpointsTags.USER_ENDPOINTS])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create new user",
    response_model=UserResponse,
)
async def create_user_instance(
    user_info: UserSchema,
    async_session: Annotated[AsyncSession, Depends(get_async_session)],
):
    if await UsersCRUD.get_user_by_email(
        async_session=async_session,
        email=user_info.email,
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Email {user_info.email} already exists.",
        )

    return {
        "status": ResponseStatuses.success,
        "user": await UsersCRUD.create_user(
            async_session=async_session,
            user_info=user_info,
        ),
    }


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get user by id",
    response_model=UserResponse,
)
async def get_user_by_id(
    user_id: int,
    async_session: Annotated[AsyncSession, Depends(get_async_session)],
):
    if not (
        user := (
            await UsersCRUD.get_user_by_id(async_session=async_session, user_id=user_id)
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with id {user_id}",
        )
    return {"status": ResponseStatuses.success, "user": user}


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Get list of users with pagination and filter",
    response_model=UsersGetResponse,
)
async def get_users(
    pagination_and_filters_params: Annotated[
        PaginationAndFiltersParams,
        Depends(PaginationAndFiltersParams),
    ],
    async_session: Annotated[AsyncSession, Depends(get_async_session)],
):
    users_info = await UsersCRUD.get_users_with_pagination_and_filters(
        async_session=async_session,
        pagination_and_filters_params=pagination_and_filters_params,
    )
    return {"status": ResponseStatuses.success, "length": len(users_info), "users": users_info}


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Update user by id",
    response_model=UserResponse,
)
async def update_user_by_id(
    user_id: int,
    new_user_data: UserWithoutValidation,
    async_session: Annotated[AsyncSession, Depends(get_async_session)],
):
    if not (
        user := (
            await UsersCRUD.get_user_by_id(async_session=async_session, user_id=user_id)
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with id {user_id}",
        )
    if await UsersCRUD.get_user_by_email(
        async_session=async_session,
        email=new_user_data.email,
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Email {new_user_data.email} already exists.",
        )
    return {
        "status": ResponseStatuses.success,
        "user": await UsersCRUD.update_user(
            async_session=async_session,
            new_user_data=new_user_data,
            current_user=user,
            user_id=user_id,
        ),
    }


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete user by id",
    response_model=UserResponse,
)
async def delete_user_by_id(
    user_id: int,
    async_session: Annotated[AsyncSession, Depends(get_async_session)],
):
    if not (
        user := (
            await UsersCRUD.get_user_by_id(async_session=async_session, user_id=user_id)
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with id {user_id}",
        )
    return {
        "status": ResponseStatuses.success,
        "user": await UsersCRUD.delete_user(async_session=async_session, user=user),
    }
