CART_URL = "/api/v1/cart"
EMPTY_CART = {"cart_items": [], "total_amount": "0.00"}

CHECKOUT_URL = f"{CART_URL}/checkout"
BILLING = {"address": "200m north of the church", "city": "Zarcero", "province": "Alajuela", "postal_code": "21101"}


def item_url(product_id: int) -> str:
    return f"{CART_URL}/items/{product_id}"

def checkout_body(**payment_overrides: object) -> dict[str, object]:
    return {"billing": BILLING, "payment": {"method": "sinpe", "reference": "20261105123456"} | payment_overrides}