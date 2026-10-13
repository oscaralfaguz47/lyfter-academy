from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.mixins import TimesTampMixin


class User(TimesTampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True)

    # This method control how the object looks when printed or logged, ex: User(id=1, email='oscar.alfaro@gmail.com') instead of <User object at...>
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"