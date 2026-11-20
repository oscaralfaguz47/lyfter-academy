""" Money rules shared by all sites. """
from decimal import Decimal, ROUND_HALF_UP

CENTS = Decimal("0.01")

def line_total(price: Decimal, quantity: Decimal) -> Decimal:
    return (price * quantity).quantize(CENTS, rounding=ROUND_HALF_UP)