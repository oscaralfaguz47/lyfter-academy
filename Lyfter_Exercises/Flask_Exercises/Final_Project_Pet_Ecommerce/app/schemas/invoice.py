from datetime import datetime
from typing import Annotated, Literal, Self, Any

from pydantic import Field, computed_field, model_validator, field_validator
from pydantic_core import PydanticCustomError

from app.models.invoice import InvoicePaymentMethod, InvoiceStatus
from app.schemas.input_schema import InputSchema
from app.schemas.pagination import PaginationParams
from app.schemas.read_schema import ReadSchema
from app.schemas.read_types import Money, Quantity


# ---------- INPUT: checkout ----------

class BillingAddressInput(InputSchema):
    # Max lengths match the invoices.billing_* columns
    address: Annotated[str, Field(min_length=1, max_length=100)]
    city: Annotated[str, Field(min_length=1, max_length=60)]
    province: Annotated[str, Field(min_length=1, max_length=60)]
    postal_code: Annotated[str, Field(min_length=1, max_length=5)]


class PaymentInput(InputSchema):
    """ The payment proof (SINPE number or card authorization code), never a card number. """
    method: InvoicePaymentMethod
    reference: Annotated[str, Field(min_length=1, max_length=40)]

    @model_validator(mode="after")
    def card_reference_is_last_four_digits(self) -> Self:
        is_four_digits = len(self.reference) == 4 and self.reference.isascii() and self.reference.isdigit()
        if self.method == InvoicePaymentMethod.CARD and not is_four_digits:
            raise PydanticCustomError("card_reference", "For card payments, reference must be exactly the last 4 digits.")
        return self


class CheckoutRequest(InputSchema):
    """ Body of POST /cart/checkout. The items come from the user's pending cart. """
    billing: BillingAddressInput
    payment: PaymentInput

class BillingAddressUpdate(InputSchema):
    address: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    city: Annotated[str, Field(min_length=1, max_length=60)] | None = None
    province: Annotated[str, Field(min_length=1, max_length=60)] | None = None
    postal_code: Annotated[str, Field(min_length=1, max_length=5)] | None = None

    @field_validator("address", "city", "province", "postal_code")
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


class InvoiceUpdate(InputSchema):
    """ Body of PATCH /invoices/<number>. Only the billing address can change (ADR-0005). """
    billing: BillingAddressUpdate


# ---------- READ ----------

class BillingAddressRead(ReadSchema):
    address: str
    city: str
    province: str
    postal_code: str


class PaymentRead(ReadSchema):
    method: InvoicePaymentMethod
    reference: str


class InvoiceLineRead(ReadSchema):
    id: int
    product_id: int
    product_name: str
    quantity: Quantity
    price: Money
    total_amount: Money


class InvoiceRead(ReadSchema):
    id: int
    invoice_number: int
    client_id: int
    cart_id: int
    status: InvoiceStatus
    total_amount: Money
    created_at: datetime
    invoice_lines: list[InvoiceLineRead]
    billing: BillingAddressRead
    payment: PaymentRead

    @model_validator(mode="before")
    @classmethod
    def group_billing_and_payment(cls, data: Any) -> Any:
        """ The model has flat columns (billing_city...) and the API groups them. """
        if isinstance(data, (dict, cls)):
            return data
        grouped = {name: getattr(data, name) for name in cls.model_fields if name not in ("billing", "payment")}
        grouped["billing"] = {
            "address": data.billing_address,
            "city": data.billing_city,
            "province": data.billing_province,
            "postal_code": data.billing_postal_code,
        }
        grouped["payment"] = {"method": data.payment_method, "reference": data.payment_reference}
        return grouped


class InvoicePage(ReadSchema):
    items: list[InvoiceRead]
    total: int


InvoiceSort = Literal["id", "-id", "invoice_number", "-invoice_number"]
class InvoiceListParams(PaginationParams):
    invoice_number: int | None = Field(default=None, ge=1)
    client_id: int | None = Field(default=None, ge=1)
    sort: InvoiceSort = "id"