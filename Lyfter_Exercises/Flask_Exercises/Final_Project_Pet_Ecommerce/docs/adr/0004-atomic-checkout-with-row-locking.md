# 0004: One transaction and row locks for checkout

**Status:** Accepted. Product locking is built, cart locking is pending.
**Date:** 2026-11-05

## Context

Checkout writes an invoice, its lines, stock and cart status. A failure halfway can't leave a sale without its stock change. Also, two people can buy the last unit at the same time, and one person can submit the same cart twice.

## Decision

- Checkout and returns run in one transaction, committed only by the service.
- Lock the cart or invoice first, then products ordered by id, with `with_for_update()`.
- Keep `CHECK (stock >= 0)` and `UNIQUE (invoices.cart_id)` as a last defense.
- Don't reserve stock when adding to a cart.

The concurrency tests in [testing.md](../testing.md#checkout) cover both cases with real threads against PostgreSQL.

## Alternatives

- **Check, then update, with no lock:** two requests can both read stock 1 and oversell.
- **Version column and retries:** works well with little contention, but needs retry code. Locks are simpler for a few rows per sale.
- **Reserving stock in the cart:** abandoned carts would block stock and need a cleanup job.

## Trade-offs

Sales of the same product wait for each other briefly. A customer can find at checkout that stock ran out, and gets a 409 with the details.
