from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimesTampMixin

if TYPE_CHECKING:
    from app.models.address import Address
    from app.models.vehicle import Vehicle


class User(TimesTampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True)

    # One user many addresses
    addresses: Mapped[list["Address"]] = relationship(back_populates="user", passive_deletes="all")

    vehicles: Mapped[list["Vehicle"]] = relationship(back_populates="user", passive_deletes="all")

    # This method control how the object looks when printed or logged, ex: User(id=1, email='oscar.alfaro@gmail.com') instead of <User object at...>
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"