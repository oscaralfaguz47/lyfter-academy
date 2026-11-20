from enum import StrEnum

from sqlalchemy import Numeric, ForeignKey, Identity, Enum, CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import AuditMixin, TimesTampMixin
from decimal import Decimal

from app.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.invoice_line import InvoiceLine
    from app.models.cart import Cart
    from app.models.invoice_return import InvoiceReturn


class InvoiceStatus(StrEnum):
    PAID = "paid"
    RETURNED = "returned"

class InvoicePaymentMethod(StrEnum):
    SINPE = "sinpe"
    CARD = "card"

class Invoice(AuditMixin, TimesTampMixin, Base):
    __tablename__ = "invoices"
    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="total_amount_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_number: Mapped[int] = mapped_column(Identity(start=100), unique=True)
    total_amount : Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[InvoiceStatus] = mapped_column(
        Enum(
            InvoiceStatus,
            name="status_valid", # name of the ck, my naming convention: ck_invoices_status_valid
            native_enum=False, # It saves the column as VARCHAR
            create_constraint=True, # It creates the CHECK(status IN('paid','returned'))
            length=10,    # Length of the varchar: VARCHAR(10)
            values_callable=lambda statuses: [s.value for s in statuses], # It gives to SQLAlchemy the list of allowed values (paid, returned)
        ),
        default=InvoiceStatus.PAID,
        server_default=InvoiceStatus.PAID.value,
    )
    billing_address: Mapped[str] = mapped_column(String(100))
    billing_city: Mapped[str] = mapped_column(String(60))
    billing_province: Mapped[str] = mapped_column(String(60))
    billing_postal_code: Mapped[str] = mapped_column(String(5))
    payment_method: Mapped[InvoicePaymentMethod] = mapped_column(
        Enum(
            InvoicePaymentMethod,
            name="payment_method_valid",
            native_enum=False,
            create_constraint=True,
            length=5,
            values_callable=lambda payment_methods: [p.value for p in payment_methods],
        ),
    )
    payment_reference: Mapped[str] = mapped_column(String(40))

    # FK Required
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)

    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="RESTRICT"), unique=True)

    # FK Relationships
    user_client: Mapped["User"] = relationship(back_populates="invoices", foreign_keys=[client_id], lazy="raise")
    cart: Mapped["Cart"] = relationship(back_populates="invoice", lazy="raise")

    # Relationships in many
    invoice_lines: Mapped[list["InvoiceLine"]] = relationship(back_populates="invoice", passive_deletes="all", lazy="raise")
    invoice_returns: Mapped[list["InvoiceReturn"]] = relationship(back_populates="invoice", passive_deletes="all", lazy="raise")
