
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.mixins import TimesTampMixin
from app.security.permissions import UserRole

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.invoice import Invoice


class User(TimesTampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), deferred=True) # Loaded only at login
    name : Mapped[str] = mapped_column(String(30))

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="role_valid", native_enum=False, create_constraint=True, length=20, values_callable=lambda roles: [r.value for r in roles]),
        default=UserRole.USER,
        server_default=UserRole.USER.value,
    )
    token_version: Mapped[int] = mapped_column(default=0, server_default="0")


