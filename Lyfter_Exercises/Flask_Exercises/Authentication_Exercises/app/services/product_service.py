
from sqlalchemy.orm import Session
from collections.abc import Sequence

from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductListParams, ProductUpdate
from app.models.product import Product
from app.errors.handlers import NotFoundError

from decimal import Decimal

import logging
logger = logging.getLogger(__name__)

class ProductService:
    def __init__(self, session: Session, repository: ProductRepository) -> None:
        self._session = session
        self._repository = repository

    def list_products(self, params: ProductListParams) -> tuple[Sequence[Product], int]:
        products = self._repository.list(params)
        return products, self._repository.count(params)

    def create_product(self, data: ProductCreate, user_id: int) -> Product:
        product = Product(**data.model_dump(), created_by_id=user_id)
        self._repository.add(product)
        self._session.commit()
        logger.info("User %s created product %s", user_id, product.id)
        return product

    def get_product(self, product_id: int) -> Product | None:
        product = self._repository.get_by_id(product_id)
        if product is None: 
            raise NotFoundError(f"Product {product_id} not found.")
        return product

    def update_product(self, product_id: int, data: ProductUpdate, user_id: int) -> Product:
        product = self.get_product(product_id)
        changes = data.model_dump(exclude_unset=True)

        for field, value in changes.items():
            setattr(product, field, value)
        product.updated_by_id = user_id

        self._repository.save(product)
        self._session.commit()
        logger.info("User %s updated product %s", user_id, product.id)
        return product

    def delete_product(self, product_id: int) -> None:
        product = self.get_product(product_id)
        self._repository.delete(product)
        self._session.commit()
        logger.info("Delete product %s", product_id)    

    def restock(self, product_id: int, quantity: Decimal, user_id: int) -> Product:
        product = self._repository.increase_stock(product_id, quantity, user_id)
        if product is None:
            raise NotFoundError(f"Product {product_id} not found.")
        self._session.commit()
        logger.info("User %s restocked product %s (+%s)", user_id, product_id, quantity)
        return product 