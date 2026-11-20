from sqlalchemy import ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.cart import Cart
    from app.models.product import Product

from decimal import Decimal

from app.database import Base


class CartItem(Base):
    __tablename__ = "cart_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="quantity_positive"),
    )

    # Composite PK: cart_id and product_id
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), primary_key=True, index=True)

    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3))

    # FK Relationship
    cart: Mapped["Cart"] = relationship(back_populates="cart_items", lazy="raise")
    product: Mapped["Product"] = relationship(back_populates="cart_items", lazy="raise")