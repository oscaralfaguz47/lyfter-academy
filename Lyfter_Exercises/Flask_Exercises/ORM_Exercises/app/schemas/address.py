from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import Annotated, TypeAlias, Self

EntityId: TypeAlias = Annotated[int, Field(gt=0)]
AddressLine: TypeAlias = Annotated[str, Field(min_length=1, max_length=200)]
City: TypeAlias = Annotated[str, Field(min_length=1, max_length=40)]
State: TypeAlias = Annotated[str, Field(min_length=1,max_length=50)]
ZipCode: TypeAlias = Annotated[str, Field(min_length=1, max_length=15)]


class InputSchema(BaseModel):
    """ Base for every request body, reject unknown fields and trim whitespace """
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

class AddressCreate(InputSchema):

    line1: AddressLine
    line2: AddressLine | None = None # Optional
    city: City
    state: State
    zip_code: ZipCode
    user_id: EntityId

class AddressUpdate(InputSchema):

    line1: AddressLine | None = None 
    line2: AddressLine | None = None # Optional
    city: City | None = None
    state: State | None = None
    zip_code: ZipCode | None = None

    @field_validator("line1", "city", "state", "zip_code")
    @classmethod
    def reject_null(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("Cannot be null.")
        return value

    @model_validator(mode="after")
    def require_at_least_one_field(self) -> Self:
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update")
        return self

class AddressRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    line1: str
    line2: str | None
    city: str
    state: str
    zip_code: str
    user_id: int
    created_at: datetime
    updated_at: datetime