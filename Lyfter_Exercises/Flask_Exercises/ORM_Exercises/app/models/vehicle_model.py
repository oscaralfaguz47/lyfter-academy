from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.brand import Brand
    from app.models.vehicle import Vehicle

from app.database import Base

class VehicleModel(Base):
    __tablename__ = "vehicle_models"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    # brand FK
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id", ondelete="RESTRICT"), index=True)

    # Relationship with brands
    brand: Mapped["Brand"] = relationship(back_populates="vehicle_models")

    # Relationship with vehicles
    vehicles: Mapped[list["Vehicle"]] = relationship(back_populates="vehicle_model", passive_deletes="all")