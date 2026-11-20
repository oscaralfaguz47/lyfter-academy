from sqlalchemy import Select, select, or_, func, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from collections.abc import Sequence
from decimal import Decimal

from app.models.product import Product
from app.schemas.product import ProductListParams
from app.errors.exceptions import ConflictError


SEARCHABLE_COLUMNS = (Product.name,)
SORT_COLUMNS = {"id": Product.id}

class ProductRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list(self, params: ProductListParams) -> Sequence[Product]:
        query = self._filtered(params).order_by(*_sort_clauses(params.sort)).offset(params.offset).limit(params.per_page)
        return self._session.scalars(query).all()

    def count(self, params: ProductListParams) -> int:
        query = self._filtered(params).with_only_columns(func.count(Product.id))
        return self._session.scalar(query) or 0

    def add(self, product: Product) -> Product:
        self._session.add(product)
        self._flush()
        return product

    def get_by_id(self, product_id: int) -> Product | None:
        return self._session.get(Product, product_id)

    def save(self, product: Product) -> Product:
        self._flush()
        return product

    def delete(self, product: Product) -> None:
        product_id = product.id
        self._session.delete(product)
        try:
            self._session.flush()
        except IntegrityError as error:
            if _violated_constraint(error) == "fk_invoice_lines_product_id_products":
                raise ConflictError(f"Product {product_id} has invoices and cannot be deleted.") from error
            raise

    def increase_stock(self, product_id: int, quantity: Decimal, user_id: int) -> Product | None:
        query = (
            update(Product)
            .where(Product.id == product_id)
            .values(stock=Product.stock + quantity, updated_by_id=user_id)
            .returning(Product)
        )
        return self._session.scalar(query)

    def get_many_for_updates(self, product_ids: list[int]) -> Sequence[Product]:
        """ Load and lock these rows until commit, equals to: (SELECT ... FOR UPDATE)"""
        """ Ordered by id, so two purchases locking the same product always lock them in the same order. """
        query = (
            select(Product)
            .where(Product.id.in_(product_ids))
            .order_by(Product.id)
            .with_for_update()
        )
        return self._session.scalars(query).all()
    

    def _filtered(self, params: ProductListParams) -> Select:
        query = select(Product)
        if params.search is not None:
            query = query.where(
                or_(*(column.icontains(params.search, autoescape=True) for column in SEARCHABLE_COLUMNS))
            )
        return query

    def _flush(self) -> None:
        try:
            self._session.flush()
        except IntegrityError as error:
            if _violated_constraint(error) == "uq_products_name":
                raise ConflictError("A product with this name already exists.") from error
            raise

def _violated_constraint(error: IntegrityError) -> str | None:
    diagnostics = getattr(error.orig, "diag", None)
    return getattr(diagnostics, "constraint_name", None)

def _sort_clauses(sort: str) -> tuple:
    column = SORT_COLUMNS[sort.lstrip("-")]
    return (column.desc() if sort.startswith("-") else column.asc(), Product.id)