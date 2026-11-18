""" Import every model here so Base.metadata knows all tables (Alembic needs this) """

from app.models.user import User
from app.models.login_history import LoginHistory
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.invoice import Invoice
from app.models.invoice_line import InvoiceLine
from app.models.product import Product
from app.models.invoice_return import InvoiceReturn
from app.models.invoice_return_line import InvoiceReturnLine

# __all__ lists what the package exports. It also tell linter "this import is used on purpose"
__all__= ["Cart", "CartItem", "Invoice", "InvoiceLine", "InvoiceReturn", "InvoiceReturnLine", "Product", "User", "LoginHistory"]