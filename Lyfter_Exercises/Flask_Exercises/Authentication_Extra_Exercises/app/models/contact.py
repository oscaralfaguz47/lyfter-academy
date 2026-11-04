from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.mixins import TimesTampMixin
from app.models.user import User


class Contact(TimesTampMixin, Base):
    __tablename__ = "contacts"
    __table_args__ = (
        UniqueConstraint("user_id", "phone", name="uq_contacts_user_id_phone"),
        UniqueConstraint("user_id", "email", name="uq_contacts_user_id_email"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(120))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)

    # relationship
    user: Mapped["User"] =  relationship(back_populates="contacts", foreign_keys=[user_id])

