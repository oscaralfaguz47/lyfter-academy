from datetime import datetime
from typing import Annotated, Self, Literal
from pydantic import Field, model_validator
from pydantic_core import PydanticCustomError

from app.schemas.input_schema import InputSchema
from app.schemas.read_schema import ReadSchema
from app.schemas.pagination import PaginationParams
from app.schemas.read_types import Money, Quantity
from app.schemas.input_types import QuantityInput

MAX_ITEMS = 50


class PurchaseItem(InputSchema):
    product_id: Annotated[int, Field(gt=0, strict=True)]
    quantity: QuantityInput

class PurchaseRequest(InputSchema):
    items: Annotated[list[PurchaseItem], Field(min_length=1, max_length=MAX_ITEMS)]

    @model_validator(mode="after")
    def no_duplicate_products(self) -> Self:
        ids = [item.product_id for item in self.items]
        if len(ids) != len(set(ids)):
            raise PydanticCustomError("duplicated_products", "Each product can appear only once.")
        return self

class InvoiceLineRead(ReadSchema):
    product_id : int
    quantity: Quantity
    price: Money
    total_amount: Money

class InvoiceRead(ReadSchema):
    id: int
    invoice_number: int
    client_id: int
    total_amount: Money
    created_at: datetime
    invoice_lines: list[InvoiceLineRead]


InvoiceSort = Literal["id", "-id", "invoice_number", "-invoice_number"]
class InvoiceListParams(PaginationParams):
    invoice_number: int | None = Field(default=None, ge=1)
    client_id: int | None = Field(default=None, ge=1)
    sort: InvoiceSort = "id"