# 0007: One pending cart per user

**Status:** Accepted. Built.
**Date:** 2026-11-17

## Context

The first design allowed several pending carts per user, at `/carts/{id}`, with `POST /carts` to create one and `GET /carts?status=pending` to go back to them. This is a single-seller pet store for end customers. A second open cart doesn't solve any problem it has, and every endpoint would need an ownership check on the cart id.

## Decision

- A user has at most one `pending` cart. The partial unique index `uq_carts_user_id_pending` (`UNIQUE (user_id) WHERE status = 'pending'`) enforces it. Completed carts aren't in the index, so a user keeps all of them as history.
- The resource is singular and always "my cart": `/cart`. The user comes from the token, never from the URL or the body, so there's no cart id to guess.
- There's no `POST /cart`. The cart is created the first time the user adds a product. `GET /cart` never creates it and returns an empty cart instead.
- `PUT /cart/items/{product_id}` sets the absolute quantity, so retrying it is safe. It uses `INSERT ... ON CONFLICT` for the cart and for the item, so two requests at the same time can't create two carts or two lines.
- `POST /cart/checkout` turns the cart into an invoice. An empty cart, or no cart at all, returns 409.
- After a checkout the cart is `completed`, and the next `PUT` creates a new pending cart.

## Alternatives

- **Several pending carts (the first design):** useful for B2B buyers or multi-store marketplaces. Here it adds an id to every route and an IDOR risk, for no business need.
- **Creating the cart with `POST /cart`:** an extra request that exposes a database detail. An empty cart and a missing cart look the same to the client.

## Trade-offs

- Admins can't read or change other users' carts through the API. Nobody needs it today.
- `GET /carts?status=pending` doesn't exist. Going back to an unfinished cart (CART-03) is `GET /cart`: the pending cart stays until it's checked out.
- Going back from one cart to several is a migration (drop the partial index) plus an id in the routes.
- A `PUT` that read the cart id right before a checkout locked the cart can still add its item to the cart that was just completed. The invoice is correct, but that item doesn't move to the new cart. Closing that window would need the `PUT` to lock the cart too.

Supersedes the multi-cart text that was in [api.md](../api.md) and [architecture.md](../architecture.md).
