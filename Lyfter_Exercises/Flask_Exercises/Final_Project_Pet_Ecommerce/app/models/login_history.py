from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import INET
from ipaddress import IPv4Address, IPv6Address

from datetime import datetime

from app.database import Base
from app.models.user import User

class LoginHistory(Base):
    __tablename__ = "login_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    login_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    user_ip: Mapped[IPv4Address | IPv6Address | None] = mapped_column(INET)
    success: Mapped[bool]

    # Relationship with users
    user: Mapped["User | None"] = relationship(back_populates="login_history", foreign_keys=[user_id], lazy="raise")