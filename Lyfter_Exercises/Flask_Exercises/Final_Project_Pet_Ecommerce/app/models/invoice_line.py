from sqlalchemy import ForeignKey, Numeric, UniqueConstraint, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

from decimal import Decimal

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.invoice import Invoice
    from app.models.product import Product

class InvoiceLine(Base):
    __tablename__ = "invoice_lines"
    __table_args__ = (
        UniqueConstraint("invoice_id", "product_id"),
        CheckConstraint("total_amount >= 0", name="total_amount_non_negative"),
        CheckConstraint("price > 0", name="price_positive"),
        CheckConstraint("quantity > 0", name="quantity_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(12,3))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    product_name: Mapped[str] = mapped_column(String(30))

    # FK for invoice
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="RESTRICT"), index=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id", ondelete="RESTRICT"))

    # Relationships with products
    product: Mapped["Product"] = relationship(back_populates="invoice_lines", lazy="raise")
    # Relationship with invoices
    invoice : Mapped["Invoice"] = relationship(back_populates="invoice_lines", lazy="raise")
