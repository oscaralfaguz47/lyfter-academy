""" Import every model here so Base.metadata knows all tables (Alembic needs this) """

from app.models.user import User
from app.models.product import Product
from app.models.invoice import Invoice
from app.models.invoice_line import InvoiceLine


# __all__ lists what the package exports. It also tell linter "this import is used on purpose"
__all__= ["User", "Invoice", "InvoiceLine", "Product"]