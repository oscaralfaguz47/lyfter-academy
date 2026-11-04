from typing import TypeAlias, Annotated, Literal
from pydantic import Field
from datetime import datetime

from app.schemas.input_schema import InputSchema
from app.schemas.read_schema import ReadSchema
from app.schemas.pagination import PaginationParams


ContactName: TypeAlias = Annotated[str, Field(min_length=1, max_length=100)]
PhoneNumber: TypeAlias = Annotated[str, Field(min_length=1, max_length=30)]
ContactEmail: TypeAlias = Annotated[str, Field(min_length=1, max_length=120)]

class ContactCreate(InputSchema):
    name: ContactName
    phone: PhoneNumber
    email: ContactEmail

class ContactRead(ReadSchema):
    id: int | None = None
    name: ContactName | None =  None
    phone: PhoneNumber | None = None
    email: ContactEmail | None = None
    created_at: datetime

ContactSort = Literal["id", "-id", "name", "-name"]
class ContactListParams(PaginationParams):
    search: str | None = Field(default=None, min_length=1, max_length=200)
    user_id: int | None = Field(default=None, ge=1)
    sort: ContactSort = "id"