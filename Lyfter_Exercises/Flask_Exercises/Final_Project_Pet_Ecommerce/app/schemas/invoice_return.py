from datetime import datetime
from typing import Annotated, Self

from pydantic import Field, computed_field, model_validator
from pydantic_core import PydanticCustomError

from app.models.invoice import InvoiceStatus
from app.schemas.input_schema import InputSchema
from app.schemas.input_types import QuantityInput
from app.schemas.read_schema import ReadSchema
from app.schemas.read_types import Money, Quantity



class ReturnLineInput(InputSchema):
    invoice_line_id: Annotated[int, Field(gt=0, strict=True)]
    quantity: QuantityInput


class InvoiceReturnRequest(InputSchema):
    """ Body of POST /invoices/<number>/returns. """
    reason: Annotated[str, Field(min_length=1, max_length=100)]
    lines: Annotated[list[ReturnLineInput], Field(min_length=1)]

    @model_validator(mode="after")
    def no_duplicate_lines(self) -> Self:
        ids = [line.invoice_line_id for line in self.lines]
        if len(ids) != len(set(ids)):
            raise PydanticCustomError("duplicated_lines", "Each invoice line can appear only once.")
        return self


class InvoiceReturnLineRead(ReadSchema):
    invoice_line_id: int
    quantity: Quantity


class _ReturnedInvoice(ReadSchema):
    invoice_number: int
    status: InvoiceStatus


class InvoiceReturnRead(ReadSchema):
    id: int
    reason: str
    refund_amount: Money
    created_at: datetime
    invoice_return_lines: list[InvoiceReturnLineRead]

    # Read from the return.invoice relationship, hidden: it comes out as invoice_number and invoice_status
    invoice: _ReturnedInvoice = Field(exclude=True)

    @computed_field
    @property
    def invoice_number(self) -> int:
        return self.invoice.invoice_number

    @computed_field
    @property
    def invoice_status(self) -> InvoiceStatus:
        return self.invoice.status