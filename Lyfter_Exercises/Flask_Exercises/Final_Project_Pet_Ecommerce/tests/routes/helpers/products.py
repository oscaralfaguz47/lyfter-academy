

PRODUCTS_URL = "/api/v1/products"
PRODUCT_FIELDS = {
    "id", "name", "price", "stock", "entry_date", "created_by_id", "updated_by_id", "created_at", "updated_at",
}


def product_body(**overrides: object) -> dict[str, object]:
    return {"name": "Carrots", "price": "5.5"} | overrides
