""" Reusable column sets for models. """
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy .orm import Mapped, mapped_column


class TimesTampMixin:
    """ Adds created_at and updated_at, filled by the database """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )