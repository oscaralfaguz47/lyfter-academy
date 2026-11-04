from typing import TypeAlias, Annotated, Literal, Self
from pydantic import Field, model_validator, field_validator
from datetime import datetime

from app.schemas.input_schema import InputSchema
from app.schemas.read_schema import ReadSchema
from app.schemas.pagination import PaginationParams
from app.schemas.user import NormalizedEmail


ContactName: TypeAlias = Annotated[str, Field(min_length=1, max_length=100)]
PhoneNumber: TypeAlias = Annotated[str, Field(min_length=1, max_length=30)]

class ContactCreate(InputSchema):
    name: ContactName
    phone: PhoneNumber
    email: NormalizedEmail

class ContactRead(ReadSchema):
    id: int
    name: str
    phone: str
    email: str
    created_at: datetime
    updated_at: datetime | None
    user_id: int


class ContactUpdate(InputSchema):
    name: ContactName | None = None
    phone: PhoneNumber | None = None
    email: NormalizedEmail | None = None

    @field_validator("name", "phone", "email")
    @classmethod
    def reject_null(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("Cannot be null.")
        return value
    
    @model_validator(mode="after")
    def require_at_least_one_field(self) -> Self:
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update.")
        return self



ContactSort = Literal["id", "-id", "name", "-name"]
class ContactListParams(PaginationParams):
    search: str | None = Field(default=None, min_length=1, max_length=200)
    user_id: int | None = Field(default=None, ge=1)
    sort: ContactSort = "id"