from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.invoice import Invoice
    from app.models.invoice_return_line import InvoiceReturnLine
    from app.models.user import User


class InvoiceReturn(Base):
    """ A return of some or all of an invoice's lines. """
    __tablename__ = "invoice_returns"
    __table_args__ = (
        CheckConstraint("refund_amount >= 0", name="refund_amount_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    reason: Mapped[str] = mapped_column(String(100))
    # Calculated once from the returned lines' frozen prices, in the same transaction, and never updated
    refund_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # FK Required
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id", ondelete="RESTRICT"), index=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)

    # FK Relationships
    invoice: Mapped["Invoice"] = relationship(back_populates="invoice_returns", lazy="raise")
    created_by: Mapped["User"] = relationship(lazy="raise")

    # Relationships in many
    invoice_return_lines: Mapped[list["InvoiceReturnLine"]] = relationship(
        back_populates="invoice_return", passive_deletes="all", lazy="raise"
    )