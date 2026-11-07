from app.cache import Cache
from app.repositories.resource_cache import ResourceCache
from app.schemas.product import ProductPage, ProductRead


class ProductCache(ResourceCache[ProductRead, ProductPage]):
    def __init__(self, cache: Cache) -> None:
        super().__init__(
            cache,
            prefix="products:v1",
            item_schema=ProductRead,
            page_schema=ProductPage,
            item_ttl_seconds=300,
            list_ttl_seconds=60,
        )