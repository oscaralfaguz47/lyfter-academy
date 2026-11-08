""" Import every model here so Base.metadata knows all tables (Alembic needs this) """

from app.models.user import User
from app.models.login_history import LoginHistory
from app.models.cart import Cart
from app.models.invoice import Invoice
from app.models.invoice_line import InvoiceLine
from app.models.product import Product

# __all__ lists what the package exports. It also tell linter "this import is used on purpose"
__all__= ["Cart", "Invoice", "InvoiceLine", "Product", "User", "LoginHistory"]