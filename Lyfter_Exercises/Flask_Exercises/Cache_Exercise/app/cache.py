import logging
import random

from flask import Flask, current_app
from redis import Redis
from redis.backoff import NoBackoff
from redis.exceptions import RedisError
from redis.retry import Retry

logger = logging.getLogger(__name__)


class Cache:
    """  If Redis is down, the app keeps working against Postgres. """
    def __init__(self, client: Redis) -> None:
        self._client = client

    def get(self, key: str) -> str | None:
        try:
            value = self._client.get(key)
        except RedisError:
            logger.warning("Cache GET failed for %s,", key, exc_info=True)
            return None
        logger.debug("Cache %s %s", "HIT" if value is not None else "MISS", key)
        return value

    def set(self, key: str, value: str, ttl_seconds: int) -> None:
        jitter = random.randint(0, ttl_seconds // 10) # 10% random to TTL, it avoids that a lot of keys expire together and hit Postgres
        try: 
            self._client.set(key, value, ex=ttl_seconds + jitter)
        except RedisError:
            logger.warning("Cache SET failed for %s", key, exc_info=True)

    def delete_and_increment(self, keys: list[str], counter_key: str) -> None:
        pipeline = self._client.pipeline(transaction=True)
        pipeline.delete(*keys)
        pipeline.incr(counter_key)
        try:
            pipeline.execute()
        except RedisError:
            logger.warning("Cache invalidation failed for %s", keys, exc_info=True)

    def ping(self) -> bool:
        try:
            return self._client.ping()
        except RedisError:
            logger.warning("Cache PING failed", exc_info=True)
            return False

def init_cache(app: Flask) -> None:
    client = Redis.from_url(
        app.config["REDIS_URL"],
        decode_responses=True,
        socket_connect_timeout=0.2,
        socket_timeout=0.2,
        retry=Retry(NoBackoff(), retries=0),
        health_check_interval=30,
    )
    app.extensions["cache"] = Cache(client)

def get_cache() -> Cache:
    return current_app.extensions["cache"]