
from typing import TYPE_CHECKING
from enum import StrEnum

from sqlalchemy import ForeignKey, Enum, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimesTampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.cart_item import CartItem


class CartStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"

class Cart(TimesTampMixin, Base):
    __tablename__ = "carts"
    __table_args__ = (
        # Unique Index constraint to allow only one 'pending' cart per user
        Index("uq_carts_user_id_pending", "user_id", unique=True, postgresql_where=text(f"status = '{CartStatus.PENDING.value}'")),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    status: Mapped[CartStatus] = mapped_column(
        Enum(
            CartStatus,
            name="status_valid", # name of the ck, my naming convention: ck_carts_status_valid
            native_enum=False, # It saves the column as VARCHAR
            create_constraint=True, # It creates the CHECK(status IN('pending','completed'))
            length=10,    # Length of the varchar: VARCHAR(10)
            values_callable=lambda statuses: [s.value for s in statuses], # It gives to SQLAlchemy the list of allowed values (pending, completed) not the name (PENDING, COMPLETED)
        ),
        default=CartStatus.PENDING,
        server_default=CartStatus.PENDING.value
    )

    # FK Relationships
    user: Mapped["User"] = relationship(back_populates="carts", foreign_keys=[user_id], lazy="raise")

    # Relationship with many
    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="cart", cascade="all, delete-orphan", passive_deletes=True, lazy="raise")
