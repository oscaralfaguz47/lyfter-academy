from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.database import Base

class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    def __repr__(self):
        return f"Brand(id={self.id}, name={self.name})"