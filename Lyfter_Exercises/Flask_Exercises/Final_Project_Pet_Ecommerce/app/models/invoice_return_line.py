from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.invoice_line import InvoiceLine
    from app.models.invoice_return import InvoiceReturn


class InvoiceReturnLine(Base):
    """ How much of one invoice line is returned in a return. """
    __tablename__ = "invoice_return_lines"
    __table_args__ = (
        # A line appears at most once per return; to return more of it later, create another return
        UniqueConstraint("invoice_return_id", "invoice_line_id"),
        CheckConstraint("quantity > 0", name="quantity_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3))

    # FK Required
    # No index=True: the unique (invoice_return_id, invoice_line_id) has it as its leftmost column
    invoice_return_id: Mapped[int] = mapped_column(ForeignKey("invoice_returns.id", ondelete="RESTRICT"))
    invoice_line_id: Mapped[int] = mapped_column(ForeignKey("invoice_lines.id", ondelete="RESTRICT"), index=True)

    # FK Relationships
    invoice_return: Mapped["InvoiceReturn"] = relationship(back_populates="invoice_return_lines", lazy="raise")
    invoice_line: Mapped["InvoiceLine"] = relationship(back_populates="invoice_return_lines", lazy="raise")