from pydantic import Field, field_validator, model_validator, PlainSerializer
from typing import Literal, Self, TypeAlias, Annotated
from datetime import datetime, date

from app.schemas.input_schema import InputSchema
from app.schemas.pagination import PaginationParams
from app.schemas.read_schema import ReadSchema
from app.schemas.read_types import Money, Quantity
from app.schemas.input_types import QuantityInput, PriceInput

ProductNameInput: TypeAlias = Annotated[str, Field(min_length=1, max_length=30)]

class ProductCreate(InputSchema):

    name: ProductNameInput
    price: PriceInput
    entry_date: date | None = None

ProductSort = Literal["id"]
class ProductListParams(PaginationParams):
    search: str | None = Field(default=None, min_length=1, max_length=200)
    sort: ProductSort = "id"


class ProductRead(ReadSchema):
    id: int
    name: str
    price: Money
    stock: Quantity
    entry_date: date 
    created_by_id: int
    updated_by_id: int | None
    created_at: datetime
    updated_at: datetime

class ProductPage(ReadSchema):
    items: list[ProductRead]
    total: int

class ProductUpdate(InputSchema):
    name: ProductNameInput | None = None
    price: PriceInput | None = None
    entry_date: date | None = None

    @field_validator("name", "price", "entry_date")
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

class IncreaseProductStock(InputSchema):
    stock: QuantityInput | None = None

    @field_validator("stock")
    @classmethod
    def reject_null(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("Cannot be null.")
        return value

    @model_validator(mode="after")
    def require_at_least_one_field(self) -> Self:
        if not self.model_fields_set:
            raise ValueError("Provide at least one field.")
        return self