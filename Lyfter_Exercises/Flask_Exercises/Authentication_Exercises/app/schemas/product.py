from pydantic import Field
from typing import Annotated, TypeAlias
from decimal import Decimal

from app.schemas.input_schema import InputSchema


ProductName : TypeAlias = Annotated[str, Field(min_length=1, max_length=30)]
Price: TypeAlias = Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
Stock: TypeAlias = Annotated[Decimal, Field(ge=0, max_digits=12, decimal_places=3)]

class ProductCreate(InputSchema):

    name: ProductName
    price: Price
    stock: Stock

