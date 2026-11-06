""" Reusable column sets for models. """
from datetime import datetime

from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy .orm import Mapped, mapped_column, relationship, declared_attr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.user import User

class TimesTampMixin:
    """ Adds created_at and updated_at, filled by the database """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

class AuditMixin:
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)
    updated_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)

    @declared_attr
    def created_by(cls) -> Mapped["User"]:
        return relationship(foreign_keys=[cls.created_by_id])

    @declared_attr
    def updated_by(cls) -> Mapped["User | None"]:
        return relationship(foreign_keys=[cls.updated_by_id])