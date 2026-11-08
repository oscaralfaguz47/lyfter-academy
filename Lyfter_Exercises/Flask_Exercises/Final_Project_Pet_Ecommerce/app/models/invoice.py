from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Numeric, ForeignKey, Identity
from app.models.mixins import AuditMixin, TimesTampMixin
from decimal import Decimal

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.invoice_line import InvoiceLine


class Invoice(AuditMixin, TimesTampMixin, Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_number: Mapped[int] = mapped_column(Identity(start=100), unique=True)
    total_amount : Mapped[Decimal] = mapped_column(Numeric(10, 2))

    # FK Required
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)

    # FK Relationships
    user_client: Mapped["User"] = relationship(back_populates="invoices", foreign_keys=[client_id])

    # Relationships in many
    invoice_lines: Mapped[list["InvoiceLine"]] = relationship(back_populates="invoice", passive_deletes="all")
