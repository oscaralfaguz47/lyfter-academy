from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic_core import PydanticCustomError
from typing import TypeAlias, Annotated, Self, Literal

from app.models.vehicle import VehicleStatus
from app.schemas.pagination import PaginationParams

EntityId: TypeAlias = Annotated[int, Field(gt=0)]
VehicleYear: TypeAlias = Annotated[int, Field(ge=1900, le=2100)]
QueryId: TypeAlias = Annotated[int, Field(gt=0)]

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


VehicleSort = Literal["id", "-id", "year", "-year"]  # Literal: only this exact values are accepted, the prefix - means descending
class VehicleListParams(PaginationParams):
    """ Query string of GET /vehicles: pagination + filters + sorting. """

    brand_id: QueryId | None = None
    model_id: QueryId | None = None
    year_min: int | None = Field(default=None, ge=1900)
    year_max: int | None = Field(default=None, ge=1900)
    has_owner: bool | None = None
    sort: VehicleSort = "id" 

    @model_validator(mode="after")
    def check_year_range(self) -> Self:
        if self.year_min is not None and self.year_max is not None and self.year_min > self.year_max:
            raise PydanticCustomError("year_range", "year_min cannot be greater than year_max.")
        return self