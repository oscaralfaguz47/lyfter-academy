
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import StrEnum

from app.database import Base
from app.models.mixins import TimesTampMixin

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.user import User


class CartStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"

class Cart(TimesTampMixin, Base):
    __tablename__ = "carts"

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
    user: Mapped["User"] = relationship(back_populates="carts", foreign_keys=[user_id])