# Caching

Redis in front of PostgreSQL using cache-aside: read Redis first, on a miss read PostgreSQL and store the result. Every write invalidates what it changed, right after the commit. Every entry also has a TTL in case an invalidation fails.

Reasons are in [ADR-0003](adr/0003-redis-cache-with-explicit-invalidation.md).

## What's cached

| Endpoint | Key | TTL | Status |
|---|---|---|---|
| `GET /products/{id}` | `products:v1:<id>` | 5 min | Built |
| `GET /products` | `products:v1:list:<version>:<hash>` | 1 min | Built |
| `GET /invoices/{number}` | `invoices:v1:<number>` | 5 min | To build |
| `GET /invoices` | `invoices:v1:list:<version>:<hash>` | 1 min | To build |

Why these:

- **Products** are the most read data in a store and they're the same for everyone. They change on writes we fully control.
- **A single invoice** barely changes after it's created, and people look it up repeatedly.
- **Invoice lists** repeat the same queries and are the example the assignment names. They're the weakest case: every sale clears them. The cost is low because they reuse the same mechanism, but under heavy sales they would rarely hit.

## What's not cached

| Endpoint | Why |
|---|---|
| Carts | They change on almost every request, so they'd rarely hit. |
| Users, `/auth/me` | Low traffic, and it's better not to copy personal data into another store. |
| The user lookup in `_authenticate` | It must stay fresh so logout and role changes apply right away. |
| Login history, returns | Low traffic. |
| `POST`, `PATCH`, `DELETE` | They change data, so they invalidate instead. |

## Invalidation

| Operation | Clears |
|---|---|
| Create, update, delete or restock a product | That product and all product lists |
| Checkout | Each purchased product, all product lists, all invoice lists |
| Return | That invoice, its products, all product and invoice lists |
| Update an invoice | That invoice, all invoice lists |

Single entries are deleted by key. Lists use a version number instead:

1. `products:v1:list_version` is part of every list key.
2. A write increments it, so all old list keys stop being read. Finding and deleting them isn't necessary.
3. The old keys expire through their TTL.

`SCAN` and `DEL` would also work but take longer as keys grow. `INCR` is one operation. `Cache.delete_and_increment` runs both steps in one Redis transaction.

`list_key` must read the version before querying PostgreSQL. If a write lands in between, the result is saved under an old version that nobody reads again.

## Why these TTLs

The TTL only covers what invalidation misses. For example, if Redis fails during an invalidation, or a read stores old data right after a write.

- **5 min for single entries:** if an invalidation is missed, old data can be served for this long, so it can't be much longer.
- **1 min for lists:** each write leaves old keys behind, and a short TTL frees that memory quickly.
- **10% random extra** in `Cache.set`, so keys created together don't all expire together and hit PostgreSQL at once.

The version counter has no TTL. Redis runs with `volatile-lru`, which only evicts keys that have a TTL, so the counter stays.

Old stock in the cache can't cause overselling, because checkout always reads stock from PostgreSQL with a lock. The worst case is a customer seeing stock that's up to 5 minutes old, and then getting a 409.

## Invoices

Add `app/repositories/invoice_cache.py` with the same structure as `product_cache.py`. Two things are different, and both matter for security:

**The ownership check runs after the cache read.** `InvoiceRead` includes `client_id`, so the service compares it on hits and misses alike. A cached invoice must not skip this check.

**The list key must include the real client id.** A client's `client_id` param is ignored, so hash the value that's actually used:

```python
client_id = params.client_id if actor.can(Permission.INVOICES_READ) else actor.id
key = self._cache.list_key(params.model_copy(update={"client_id": client_id}))
```

Without this, two clients with the same params would share a key and see each other's invoices.

## When Redis fails

`Cache` catches every `RedisError`, and the client times out after 0.2 seconds.

| Case | What happens |
|---|---|
| Read fails | Logs a warning and reads PostgreSQL. |
| Write fails | Logs a warning. The next read is another miss. |
| Invalidation fails | Logs a warning. Old data can stay until its TTL. |
| `/health` | Reports `"cache": "unreachable"`. |
