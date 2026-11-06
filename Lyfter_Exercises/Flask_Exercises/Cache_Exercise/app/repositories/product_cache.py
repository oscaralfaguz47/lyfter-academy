import hashlib
import logging
import pydantic

from app.cache import Cache
from app.schemas.product import ProductListParams, ProductPage, ProductRead

logger = logging.getLogger(__name__)

KEY_PREFIX = "products:v1"
LIST_VERSION_KEY = f"{KEY_PREFIX}:list_version"
PRODUCT_TTL_SECONDS = 300
LIST_TTL_SECONDS = 60

class ProductCache:
    def __init__(self, cache: Cache) -> None:
        self._cache = cache

    def get_product(self, product_id: int) -> ProductRead | None:
        return _decode(ProductRead, self._cache.get(_product_key(product_id)))

    def set_product(self, product: ProductRead) -> None:
        self._cache.set(_product_key(product.id), product.model_dump_json(), PRODUCT_TTL_SECONDS)

    def list_key(self, params: ProductListParams) -> str:
        """ Call this before reading Postgres, so a write in between makes this key obsolete. """
        version = self._cache.get(LIST_VERSION_KEY) or "0"
        params_hash = hashlib.sha256(params.model_dump_json().encode()).hexdigest()
        return f"{KEY_PREFIX}:list:{version}:{params_hash}"

    def get_list(self, key: str) -> ProductPage | None:
        return _decode(ProductPage, self._cache.get(key))

    def set_list(self, key: str, page: ProductPage) -> None:
        self._cache.set(key, page.model_dump_json(), LIST_TTL_SECONDS)

    def invalidate(self, *product_ids: int) -> None:
        """ Call this after commit. """
        keys = [_product_key(product_id) for product_id in product_ids]
        self._cache.delete_and_increment(keys, LIST_VERSION_KEY)




def _product_key(product_id: int) -> str:
    return f"{KEY_PREFIX}:{product_id}"

def _decode[SchemaT: pydantic.BaseModel](schema: type[schema], cached: str | None) -> SchemaT | None:
    if cached is None:
        return None
    try:
        return schema.model_validate_json(cached)
    except pydantic.ValidationError:
        logger.warning("Ignoring invalid cache entry for %s", schema.__name__)
        return None