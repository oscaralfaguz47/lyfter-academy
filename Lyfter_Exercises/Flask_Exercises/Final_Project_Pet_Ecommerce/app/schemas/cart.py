from decimal import Decimal
from pydantic import computed_field
from datetime import datetime

from app.domain.pricing import line_total
from app.schemas.read_schema import ReadSchema
from app.schemas.types import Money, Quantity


class CartProductRead(ReadSchema):
    id: int
    name: str
    price: Money

class CartItemRead(ReadSchema):
    product: CartProductRead
    quantity: Quantity

    # @computed_field + @property: Pydantic includes the calculated value (total_amount) in the JSON even if it doesn't exist in the model.
    @computed_field
    @property
    def total_amount(self) -> Money:
        return line_total(self.product.price, self.quantity)

class CartRead(ReadSchema):
    cart_items: list[CartItemRead]

    @computed_field
    @property
    def total_amount(self) -> Money:
        return sum((item.total_amount for item in self.cart_items), Decimal(0))

