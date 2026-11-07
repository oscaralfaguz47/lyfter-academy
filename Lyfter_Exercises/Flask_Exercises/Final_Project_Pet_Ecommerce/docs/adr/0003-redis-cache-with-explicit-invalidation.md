# 0003: Redis with invalidation and TTL

**Status:** Accepted. Built for products, invoices pending.
**Date:** 2026-11-05

## Context

Products are read far more often than they change. Invoices barely change once created. But stock changes with every sale, so a cached product can quickly be wrong. The assignment asks for invalidation rules and a TTL decision.

## Decision

Cache-aside in Redis, for products and invoices. Writes invalidate after the commit. Every entry also has a TTL as a backup. Lists use a version number in the key. Redis failures never break a request. Details are in [caching.md](../caching.md).

## Alternatives

- **TTL only:** customers would see wrong stock until it expires.
- **Invalidation only:** one failed invalidation leaves wrong data forever.
- **`SCAN` and `DEL` for lists:** works, but the cost grows with the number of keys. A version bump is one `INCR`.
- **Memory inside the process:** each worker would have its own copy and invalidation wouldn't reach the others.
- **Caching carts:** they change on almost every request.

## Trade-offs

Each new write has to remember to invalidate, so the tests cover it. Redis is one more service to run. A small race remains: a read can store old data right after a write. The TTL limits that to 5 minutes, and checkout is safe anyway because it reads stock from PostgreSQL.
