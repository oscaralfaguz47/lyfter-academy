from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import SmallInteger, Enum, ForeignKey

from app.models.mixins import TimesTampMixin
from app.models.enums import VehicleStatus
from app.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.vehicle_model import VehicleModel
    from app.models.user import User



class Vehicle(TimesTampMixin, Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(SmallInteger)
    status: Mapped[VehicleStatus] = mapped_column(
        Enum(
            VehicleStatus,
            name="status",
            native_enum=False, 
            create_constraint=True,
            length=20,
            values_callable=lambda enum: [member.value for member in enum],
        ),
        default=VehicleStatus.AVAILABLE,
        server_default=VehicleStatus.AVAILABLE.value
    )

    # Required FK vehicle_model
    model_id: Mapped[int] = mapped_column(ForeignKey("vehicle_models.id", ondelete="RESTRICT"), index=True)
    # optional FK user
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)

    #Relationships
    vehicle_model: Mapped["VehicleModel"] = relationship(back_populates="vehicles")
    user: Mapped["User | None"] = relationship(back_populates="vehicles")