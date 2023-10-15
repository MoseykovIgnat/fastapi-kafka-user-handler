from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator
import pytz


class User(BaseModel):
    name: str = Field(title="Name of user")
    surname: str = Field(title="Surname of user")
    email: EmailStr = Field(title="Email of user")
    birthday: datetime = Field(title="Birthday date of user")

    @field_validator("birthday")
    def dt_validate(cls, birthday: datetime) -> datetime:  # noqa
        return birthday.astimezone(pytz.UTC).replace(tzinfo=None)


class ModelUser(User):
    user_id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class BaseResponse(BaseModel):
    status: str


class UserResponse(BaseResponse):
    user: ModelUser


class UsersGetResponse(BaseResponse):
    length: int
    users: list[ModelUser]
