from app.database import Base
from app.models.mixins import TimesTampMixin, AuditMixin
from decimal import Decimal

from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column


class Product(AuditMixin, TimesTampMixin, Base):
    __tablename__ = "products"

    id : Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock: Mapped[Decimal] = mapped_column(Numeric(12,3), default=0, server_default="0")
