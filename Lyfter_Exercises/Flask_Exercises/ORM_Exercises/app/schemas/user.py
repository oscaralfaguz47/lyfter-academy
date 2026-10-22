""" Shapes the user data that enters and leaves the API """

from datetime import datetime
from typing import Annotated, TypeAlias, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, AfterValidator, model_validator

from app.schemas.pagination import PaginationParams

# Reusable type, a valid email and lowercased
NormalizedEmail: TypeAlias = Annotated[EmailStr, AfterValidator(str.lower), Field(max_length=120)]
UserName: TypeAlias = Annotated[str, Field(min_length=1, max_length=100)]

class UserCreate(BaseModel):
    """ Body of POST /users """

    # extra="forbid": unknown fields are rejected
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: UserName
    # EmailStr validates the email format
    email: NormalizedEmail


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: UserName | None = None
    email: NormalizedEmail | None = None

    @field_validator("name", "email")
    @classmethod
    def reject_null(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("Cannot be null.")
        return value

    @model_validator(mode="after")
    def require_at_least_one_field(self) -> "UserUpdate":
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update.")
        return self


class UserRead(BaseModel):
    """ What the API returns for a user, never includes sensitive fields """

    model_config = ConfigDict(from_attributes=True) # Read from a SQLAlchemy object instead of only from dicts, ex: user.name

    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime


UserSort = Literal["id", "-id", "name", "-name"]
class UserListParams(PaginationParams):
    min_vehicles: int | None = Field(default=None, ge=1)
    sort: UserSort = "id"