# 0005: Invoice snapshots and restricted deletes

**Status:** Accepted. The price snapshot and `RESTRICT` are built, the rest is pending.
**Date:** 2026-11-05

## Context

An invoice must always show what was bought and paid, but admins can edit and delete products. The assignment also lists delete endpoints for invoices, but deleting a sale would erase its financial record.

## Decision

1. `invoice_lines` copies `product_name` and `price` at checkout. Invoices store their total and billing address.
2. Sold products and users with history can't be deleted (`RESTRICT`, 409). Unsold products can.
3. There's no `DELETE /invoices/{number}`. To cancel a sale, an admin returns every line, which restores the stock and sets the invoice to `returned`. Invoice statuses are only `paid` and `returned`.
4. Invoices are only created through checkout, which clients can use. There's no `POST /invoices`.

## Alternatives

- **Read the current price from `products`:** fully normalized, but a price change would rewrite old invoices.
- **Soft delete with `is_active`:** lets you retire sold products, but every product query must then filter on it, and carts need extra rules. Not worth it here, and a product can be left at stock 0.
- **`CASCADE` or `SET NULL`:** would delete invoice lines or lose what was sold.
- **Admin-only `POST /invoices`:** would allow invoices with no sale and no stock change.
- **`DELETE` that removes the invoice:** loses the record of the sale.
- **`DELETE` that voids the invoice:** keeps the record, but adds a `voided` status and a second way to restore stock that does the same as a full return.

## Trade-offs

Sold products stay in the catalog with no way to hide them. If that becomes a problem, add `is_active` in a new decision.

Invoices don't follow the full CRUD the assignment lists. A full return covers the same need and keeps one path for restoring stock.
