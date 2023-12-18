from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class ResponseValidators:
    """Class with methods to validate process ML request (Tariffs or Antifraud) json"""

    @staticmethod
    def dt_validate(birthday: datetime) -> datetime:  # noqa
        return birthday.replace(tzinfo=None)


class UserWithoutValidation(BaseModel):
    name: str | None = Field(title="Name of user", default=None)
    surname: str | None = Field(title="Surname of user", default=None)
    email: EmailStr | None = Field(title="Email of user", default=None)
    birthday: datetime | None = Field(title="Birthday date of user", default=None)

    model_config = ConfigDict(
        populate_by_name=True,
    )

    _ = field_validator(
        "birthday",
    )(ResponseValidators.dt_validate)


class User(BaseModel):
    name: str = Field(title="Name of user", validation_alias="Name", alias_priority=0)
    surname: str = Field(title="Surname of user", validation_alias="Surname")
    email: EmailStr = Field(title="Email of user", validation_alias="Email")
    birthday: datetime = Field(
        title="Birthday date of user",
        validation_alias="Birthday",
    )

    model_config = ConfigDict(
        populate_by_name=True,
    )

    _ = field_validator(
        "birthday",
    )(ResponseValidators.dt_validate)


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
