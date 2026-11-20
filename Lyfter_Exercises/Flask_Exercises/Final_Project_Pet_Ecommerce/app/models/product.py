from decimal import Decimal
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import String, Numeric, Date, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimesTampMixin, AuditMixin

if TYPE_CHECKING:
    from app.models.cart_item import CartItem
    from app.models.invoice_line import InvoiceLine


class Product(AuditMixin, TimesTampMixin, Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("price > 0", name="price_positive"),
        CheckConstraint("stock >= 0", name="stock_non_negative"),
    )

    id : Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock: Mapped[Decimal] = mapped_column(Numeric(12,3), default=0, server_default="0")
    entry_date: Mapped[date] = mapped_column(Date, server_default=func.current_date())

    # Relationship in many
    invoice_lines: Mapped[list["InvoiceLine"]] = relationship(back_populates="product", passive_deletes="all", lazy="raise")
    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="product", passive_deletes="all", lazy="raise")

