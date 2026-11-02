from flask import Blueprint, request, url_for

from app.services.product_service import ProductService
from app.database import get_session
from app.repositories.product_repository import ProductRepository
from app.schemas.validation import parse
from app.schemas.product import ProductRead, ProductListParams, ProductCreate, ProductUpdate, IncreaseProductStock
from app.routes.responses import pagination_meta, serialize_many, ok, serialize, created, no_content
from app.auth import login_required, current_user_id


products_bp = Blueprint("products", __name__, url_prefix="/api/v1/products")

def _product_service() -> ProductService:
    session = get_session()
    return ProductService(session, ProductRepository(session))

@products_bp.get("")
@login_required
def list_products():
    params = parse(ProductListParams, request.args.to_dict(), "Invalid query params.")
    products, total = _product_service().list_products(params)
    meta = pagination_meta(params.page, params.per_page, total)
    return ok(serialize_many(ProductRead, products), meta=meta)

@products_bp.get("/<int:product_id>")
@login_required
def get_product(product_id: int):
    product = _product_service().get_product(product_id)
    return ok(serialize(ProductRead, product))

@products_bp.post("")
@login_required
def create_product():
    data = parse(ProductCreate, request.get_json())
    product = _product_service().create_product(data, current_user_id())
    return created(serialize(ProductRead, product), location=url_for("products.get_product", product_id=product.id))

@products_bp.patch("/<int:product_id>")
@login_required
def update_product(product_id: int):
    data = parse(ProductUpdate, request.get_json())
    product = _product_service().update_product(product_id, data, current_user_id())
    return ok(serialize(ProductRead, product))

@products_bp.delete("/<int:product_id>")
@login_required
def delete_product(product_id: int):
    _product_service().delete_product(product_id)
    return no_content()

@products_bp.patch("/<int:product_id>/restock")
@login_required
def restock_product(product_id: int):
    data = parse(IncreaseProductStock, request.get_json())
    product = _product_service().restock(product_id, data.stock, current_user_id())
    return ok(serialize(ProductRead, product))