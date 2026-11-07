import hashlib
import logging

import pydantic

from app.cache import Cache

logger = logging.getLogger(__name__)


class ResourceCache[ItemT: pydantic.BaseModel, PageT: pydantic.BaseModel]:
    def __init__(
            self, 
            cache: Cache,
            *,
            prefix: str,
            item_schema: type[ItemT],
            page_schema: type[PageT],
            item_ttl_seconds: int,
            list_ttl_seconds: int
    ) -> None:
        self._cache = cache
        self._prefix = prefix
        self._item_schema = item_schema
        self._page_schema = page_schema
        self._item_ttl_seconds = item_ttl_seconds
        self._list_ttl_seconds = list_ttl_seconds
        self._list_version_key = f"{prefix}:list_version"

    def get_item(self, item_id: int) -> ItemT | None:
        return _decode(self._item_schema, self._cache.get(self._item_key(item_id)))

    def set_item(self, item_id: int, item: ItemT) -> None:
        self._cache.set(self._item_key(item_id), item.model_dump_json(), self._item_ttl_seconds)

    def list_key(self, params: pydantic.BaseModel) -> str:
        """ Call this before reading the database. """
        version = self._cache.get(self._list_version_key) or "0"
        params_hash = hashlib.sha256(params.model_dump_json().encode()).hexdigest()
        return f"{self._prefix}:list:{version}:{params_hash}"

    def get_list(self, key: str) -> PageT | None:
        return _decode(self._page_schema, self._cache.get(key))

    def set_list(self, key: str, page: PageT) -> None:
        self._cache.set(key, page.model_dump_json(), self._list_ttl_seconds)

    def invalidate(self, *item_ids: int) -> None:
        """ Call this AFTER commit. """
        keys = [self._item_key(item_id) for item_id in item_ids]
        self._cache.delete_and_increment(keys, self._list_version_key)

    def _item_key(self, item_id: int) -> str:
        return f"{self._prefix}:{item_id}"



def _decode[SchemaT: pydantic.BaseModel](schema: type[SchemaT], cached: str | None) -> SchemaT | None:
    if cached is None:
        return None
    try:
        return schema.model_validate_json(cached)
    except pydantic.ValidationError:
        logger.warning("Ignoring invalid cache entry for %s", schema.__name__)
        return None