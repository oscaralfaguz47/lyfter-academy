""" Import every model here so Base.metadata knows all tables (Alembic needs this) """

from app.models.user import User


# __all__ lists what the package exports. It also tell linter "this import is used on purpose"
__all__= ["User"]