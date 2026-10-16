from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from app.models.mixins import TimesTampMixin
from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Address(TimesTampMixin, Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    line1: Mapped[str] = mapped_column(String(200))
    line2: Mapped[str | None] = mapped_column(String(200))
    city: Mapped[str] = mapped_column(String(40))
    state: Mapped[str] = mapped_column(String(50))
    zip_code: Mapped[str] = mapped_column(String(15))
    # Users FK
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)

    # The relationship, this is a Python shortcut to the related object
    user: Mapped["User"] = relationship(back_populates="addresses")


    def __repr__(self):
        return f"Address(id={self.id!r}, user_id={self.user_id!r}"