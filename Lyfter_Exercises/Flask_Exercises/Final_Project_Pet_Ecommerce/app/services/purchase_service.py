from sqlalchemy.orm import Session
from decimal import Decimal
from collections.abc import Sequence
from app.errors.exceptions import ConflictError, ValidationError, NotFoundError

from app.domain.pricing import line_total

import logging
logger = logging.getLogger(__name__)


from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.cart_repository import CartRepository
from app.repositories.product_cache import ProductCache
from app.schemas.invoice import PurchaseRequest, InvoiceListParams
from app.security.permissions import Actor, Permission
from app.models.invoice import Invoice
from app.models.invoice_line import InvoiceLine
from app.models.product import Product
from app.models.cart import CartStatus


class PurchaseService:
    def __init__(
            self, session: Session, 
            product_repository: ProductRepository, 
            invoice_repository: InvoiceRepository, 
            cart_repository: CartRepository,
            product_cache: ProductCache
            ) -> None:
        self._session = session
        self._product_repository = product_repository
        self._invoice_repository = invoice_repository
        self._cart_repository = cart_repository
        self._product_cache = product_cache

    def purchase(self, data: PurchaseRequest, actor: Actor) -> Invoice:
        quantities = {item.product_id: item.quantity for item in data.items}

        # Load and lock every product.
        products = self._product_repository.get_many_for_updates(list(quantities))
        _ensure_all_exist(quantities, products)
        _ensure_enough_stock(quantities, products)

        # Build the invoice with prices from the database.
        invoice = Invoice(client_id=actor.id, total_amount=Decimal(0), created_by_id=actor.id)
        for product in products:
            quantity = quantities[product.id]
            line_total_amount = line_total(product.price, quantity)
            invoice.invoice_lines.append(
                InvoiceLine(product_id=product.id, quantity=quantity, price=product.price, total_amount=line_total_amount)
            )
            invoice.total_amount += line_total_amount
            product.stock -= quantity
        # One commit for everything, invoice, invoice_lines and product.stock
        self._invoice_repository.add(invoice)
        self._session.commit()
        self._product_cache.invalidate(*quantities)
        logger.info("User %s bought %s products (invoice %s, total %s)", actor.id, len(products), invoice.id, invoice.total_amount)
        return invoice

    def checkout(self, actor: Actor) -> Invoice:
        """ Buy everything in the user's pending cart and close it, all in one transaction. """
        # Lock order: the cart first, then the products (inside _build_invoice). Same order everywhere = no deadlocks
        cart = self._cart_repository.get_pending_by_user_for_update(actor.id)
        if cart is None or not cart.cart_items:
            raise ConflictError("Your cart is empty.")

        quantities = {item.product_id: item.quantity for item in cart.cart_items}
        invoice = self._build_invoice(quantities, actor)
        cart.status = CartStatus.COMPLETED
        self._session.commit() # One commit: invoice, invoice_lines, product.stock and the cart status
        self._product_cache.invalidate(*quantities)
        logger.info("User %s checked out cart %s (invoice %s, total %s)", actor.id, cart.id, invoice.id, invoice.total_amount)
        return invoice

    def _build_invoice(self, quantities: dict[int, Decimal], actor: Actor) -> Invoice:
        """ Lock the products, validate them, build the invoice with database prices and take the stock. """
        """ It never commits, the caller owns the transaction, so it can add its own changes to the same commit. """
        products = self._product_repository.get_many_for_updates(list(quantities))
        _ensure_all_exist(quantities, products)
        _ensure_enough_stock(quantities, products)

        invoice = Invoice(client_id=actor.id, total_amount=Decimal(0), created_by_id=actor.id)
        for product in products:
            quantity = quantities[product.id]
            line_total_amount = line_total(product.price, quantity)
            invoice.invoice_lines.append(
                InvoiceLine(product_id=product.id, quantity=quantity, price=product.price, total_amount=line_total_amount)
            )
            invoice.total_amount += line_total_amount
            product.stock -= quantity
        self._invoice_repository.add(invoice) # flush, not commit, assigns invoice.id and maps constraint errors
        return invoice
        
    def get_invoice(self, invoice_id: int, actor: Actor) -> Invoice:
        invoice = self._invoice_repository.get_by_id(invoice_id)
        if invoice is None or (invoice.client_id != actor.id and not actor.can(Permission.INVOICES_READ)):
            raise NotFoundError(f"Invoice {invoice_id} not found.")
        return invoice

    def list_invoices(self, params: InvoiceListParams, actor: Actor) -> tuple[Sequence[Invoice], int]:
        client_id = params.client_id if actor.can(Permission.INVOICES_READ) else actor.id  # The user sees their own invoices and Admin sees all
        invoices = self._invoice_repository.list(params, client_id)
        return invoices, self._invoice_repository.count(params, client_id)



def _ensure_all_exist(quantities: dict[int, Decimal], products: Sequence[Product]) -> None:
    missing = sorted(set(quantities) - {product.id for product in products})
    if missing: 
        raise ValidationError("Some products don't exist.", details={"product_ids": missing})

def _ensure_enough_stock(quantities: dict[int, Decimal], products: Sequence[Product]) -> None:
    short = [
        {"product_id": p.id, "requested": str(quantities[p.id]), "available": str(p.stock)}
        for p in products
        if p.stock < quantities[p.id]
    ]
    if short:
        raise ConflictError("Not enough stock.", details={"products": short})