""" Shapes the user data that enters and leaves the API """

from datetime import datetime
from typing import Literal, TypeAlias, Annotated

from pydantic import BaseModel, ConfigDict, field_validator, model_validator, computed_field, Field

from app.schemas.pagination import PaginationParams
from app.schemas.input_types import PhoneNumberInput, NormalizedEmailInput
from app.security.permissions import UserRole, Permission, ROLE_PERMISSIONS

UserNameInput: TypeAlias = Annotated[str, Field(min_length=1, max_length=100)]


class UserCreate(BaseModel):
    """ Fields shared by every way of creating a user, Base of RegisterRequest.  """

    # extra="forbid": unknown fields are rejected
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: UserNameInput
    phone_number: PhoneNumberInput
    # EmailStr validates the email format
    email: NormalizedEmailInput


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: UserNameInput | None = None
    phone_number: PhoneNumberInput | None = None
    email: NormalizedEmailInput | None = None

    @field_validator("name", "email", "phone_number")
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
    phone_number: str
    email: str
    created_at: datetime
    updated_at: datetime
    role: UserRole

class MeRead(UserRead):
    @computed_field
    @property
    def permissions(self) -> list[Permission]:
        return sorted(ROLE_PERMISSIONS[self.role])


UserSort = Literal["id", "-id", "name", "-name"]
class UserListParams(PaginationParams):
    sort: UserSort = "id"

