from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import TypeAlias, Annotated, Self

from app.models.vehicle import VehicleStatus

EntityId: TypeAlias = Annotated[int, Field(gt=0)]
VehicleYear: TypeAlias = Annotated[int, Field(ge=1900, le=2100)]

class InputSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

class BrandRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

class VehicleModelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    brand: BrandRead

class VehicleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    year: int
    status: VehicleStatus
    vehicle_model: VehicleModelRead
    user_id: int | None
    created_at: datetime
    updated_at: datetime

class VehicleCreate(InputSchema):

    year: VehicleYear
    model_id: EntityId

class VehicleUpdate(InputSchema):

    year: VehicleYear | None = None
    model_id: EntityId | None = None

    @field_validator("year", "model_id")
    @classmethod
    def reject_null(cls, value: int | None) -> int:
        if value is None:
            raise ValueError("Cannot be null.")
        return value

    @model_validator(mode="after")
    def required_at_least_one_field(self) -> Self:
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update.")
        return self

class VehicleOwnerAssign(InputSchema):
    user_id: EntityId