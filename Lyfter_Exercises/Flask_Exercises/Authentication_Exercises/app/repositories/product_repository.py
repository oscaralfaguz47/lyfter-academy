from sqlalchemy import Select, select, or_, func, update
from sqlalchemy.orm import Session
from collections.abc import Sequence
from decimal import Decimal

from app.models.product import Product
from app.schemas.product import ProductListParams


SEARCHABLE_COLUMNS = (Product.name)
SORT_COLUMNS = {"id": Product.id}

class ProductRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list(self, params: ProductListParams) -> Sequence[Product]:
        query = self._filtered(params).order_by(*_sort_clauses(params.sort)).offset(params.offset).limit(params.per_page)
        return self._session.scalars(query) or 0

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
        self._session.delete(product)
        self._session.flush()

    def increase_stock(self, product_id: int, quantity: Decimal, user_id: int) -> Product | None:
        query = (
            update(Product)
            .where(Product.id == product_id)
            .values(stock=Product.stock + quantity, updated_by_id=user_id)
            .returning(Product)
        )
        return self._session.scalar(query)

    def _filtered(self, params: ProductListParams) -> Select:
        query = select(Product)
        if params.search is not None:
            query = query.where(
                or_(*(column.icontains(params.search, autoescape=True) for column in SEARCHABLE_COLUMNS))
            )
        return query

    def _flush(self) -> None:
        self._session.flush()



def _sort_clauses(sort: str) -> tuple:
    column = SORT_COLUMNS[sort.lstrip("-")]
    return (column.desc() if sort.startswith("-") else column.asc(), Product.id)