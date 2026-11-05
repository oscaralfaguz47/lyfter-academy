from pydantic import Field, field_validator, model_validator
from typing import Annotated, TypeAlias, Literal, Self
from decimal import Decimal
from datetime import datetime, date

from app.schemas.input_schema import InputSchema
from app.schemas.pagination import PaginationParams
from app.schemas.read_schema import ReadSchema


ProductName : TypeAlias = Annotated[str, Field(min_length=1, max_length=30)]
Price: TypeAlias = Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
Stock: TypeAlias = Annotated[Decimal, Field(gt=0, max_digits=12, decimal_places=3)]

class ProductCreate(InputSchema):

    name: ProductName
    price: Price
    entry_date: date | None = None

ProductSort = Literal["id"]
class ProductListParams(PaginationParams):
    search: str | None = Field(default=None, min_length=1, max_length=200)
    sort: ProductSort = "id"


class ProductRead(ReadSchema):
    id: int
    name: str
    price: Decimal
    stock: Decimal
    entry_date: date 
    created_by_id: int
    updated_by_id: int | None
    created_at: datetime
    updated_at: datetime

class ProductPage(ReadSchema):
    items: list[ProductRead]
    total: int

class ProductUpdate(InputSchema):
    name: ProductName | None = None
    price: Price | None = None
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
    stock: Stock | None = None

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