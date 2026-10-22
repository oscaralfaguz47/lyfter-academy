""" Import every model here so Base.metadata knows all tables (Alembic needs this) """

from app.models.user import User
from app.models.address import Address
from app.models.brand import Brand
from app.models.vehicle import Vehicle
from app.models.vehicle_model import VehicleModel


# __all__ lists what the package exports. It also tell linter "this import is used on purpose"
__all__= ["Address", "Brand", "User", "Vehicle", "VehicleModel"]