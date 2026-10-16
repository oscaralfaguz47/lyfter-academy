from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from app.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.vehicle_model import VehicleModel

class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    # Relationship with models

    vehicle_models: Mapped[list["VehicleModel"]] = relationship(back_populates="brand", passive_deletes="all")

    def __repr__(self):
        return f"Brand(id={self.id}, name={self.name})"