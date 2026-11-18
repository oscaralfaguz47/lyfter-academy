import logging
from collections.abc import Sequence
from decimal import Decimal

from sqlalchemy.orm import Session

from app.domain.pricing import line_total
from app.errors.exceptions import ConflictError, NotFoundError, ValidationError
from app.models.cart import Cart, CartStatus
from app.models.invoice import Invoice
from app.models.invoice_line import InvoiceLine
from app.models.product import Product
from app.repositories.cart_repository import CartRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.product_cache import ProductCache
from app.repositories.product_repository import ProductRepository
from app.schemas.invoice import CheckoutRequest, InvoiceListParams, InvoiceUpdate
from app.security.permissions import Actor, Permission

logger = logging.getLogger(__name__)


class PurchaseService:
    def __init__(
            self,
            session: Session,
            product_repository: ProductRepository,
            invoice_repository: InvoiceRepository,
            cart_repository: CartRepository,
            product_cache: ProductCache,
            ) -> None:
        self._session = session
        self._product_repository = product_repository
        self._invoice_repository = invoice_repository
        self._cart_repository = cart_repository
        self._product_cache = product_cache

    def checkout(self, data: CheckoutRequest, actor: Actor) -> Invoice:
        """ Buy everything in the user's pending cart and close it, all in one transaction. """
        # Lock order: the cart first, then the products (inside _build_invoice). Same order everywhere = no deadlocks.
        cart = self._cart_repository.get_pending_by_user_for_update(actor.id)
        if cart is None or not cart.cart_items:
            raise ConflictError("Your cart is empty.")

        invoice = self._build_invoice(cart, data, actor)
        cart.status = CartStatus.COMPLETED
        self._session.commit()  # One commit: invoice, invoice_lines, product.stock and the cart status
        self._product_cache.invalidate(*(item.product_id for item in cart.cart_items))
        logger.info("User %s checked out cart %s (invoice %s, total %s)", actor.id, cart.id, invoice.id, invoice.total_amount)
        return invoice

    def get_invoice(self, invoice_number: int, actor: Actor) -> Invoice:
        """ Someone else's invoice returns the same 404 as a missing one, so its existence isn't revealed. """
        invoice = self._invoice_repository.get_by_number(invoice_number)
        if invoice is None or (invoice.client_id != actor.id and not actor.can(Permission.INVOICES_READ)):
            raise NotFoundError(f"Invoice {invoice_number} not found.")
        return invoice

    def update_billing(self, invoice_number: int, data: InvoiceUpdate, actor: Actor) -> Invoice:
        """ Fix the billing address of an invoice. Amounts, lines and payment never change, those are fixed with a return. """
        invoice = self._invoice_repository.get_by_number(invoice_number)
        if invoice is None:
            raise NotFoundError(f"Invoice {invoice_number} not found.")
        for field, value in data.billing.model_dump(exclude_unset=True).items():
            setattr(invoice, f"billing_{field}", value)  # billing.city -> invoices.billing_city
        invoice.updated_by_id = actor.id
        self._session.commit()
        logger.info("User %s updated the billing of invoice %s", actor.id, invoice_number)
        return invoice

    def list_invoices(self, params: InvoiceListParams, actor: Actor) -> tuple[Sequence[Invoice], int]:
        client_id = params.client_id if actor.can(Permission.INVOICES_READ) else actor.id  # The user sees their own invoices and Admin sees all
        invoices = self._invoice_repository.list(params, client_id)
        return invoices, self._invoice_repository.count(params, client_id)

    def _build_invoice(self, cart: Cart, data: CheckoutRequest, actor: Actor) -> Invoice:
        """ Lock the products, validate them, build the invoice with database prices and take the stock.
            It never commits: checkout owns the transaction and adds the cart status to the same commit. """
        quantities = {item.product_id: item.quantity for item in cart.cart_items}
        products = self._product_repository.get_many_for_updates(list(quantities))
        _ensure_all_exist(quantities, products)
        _ensure_enough_stock(quantities, products)

        invoice = Invoice(
            client_id=actor.id,
            created_by_id=actor.id,
            cart_id=cart.id,
            total_amount=Decimal(0),
            billing_address=data.billing.address,
            billing_city=data.billing.city,
            billing_province=data.billing.province,
            billing_postal_code=data.billing.postal_code,
            payment_method=data.payment.method,
            payment_reference=data.payment.reference,
        )
        for product in products:
            quantity = quantities[product.id]
            line_total_amount = line_total(product.price, quantity)
            invoice.invoice_lines.append(
                InvoiceLine(
                    product_id=product.id,
                    product_name=product.name,  # Snapshot, a later rename doesn't change this invoice
                    quantity=quantity,
                    price=product.price,        # Snapshot, a later price change doesn't change this invoice
                    total_amount=line_total_amount,
                )
            )
            invoice.total_amount += line_total_amount
            product.stock -= quantity
        self._invoice_repository.add(invoice)  # flush, not commit: assigns invoice.id and maps constraint errors
        return invoice


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