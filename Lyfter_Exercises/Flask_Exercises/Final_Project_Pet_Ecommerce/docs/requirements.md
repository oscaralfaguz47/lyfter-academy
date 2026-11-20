# Requirements


## Users and authentication

| ID | Requirement | Status |
|---|---|---|
| AUTH-01 | Register. New accounts are clients. | Done ✔|
| AUTH-02 | Log in and receive tokens. | Done ✔ |
| AUTH-03 | Validate the token on every request to other modules. | Done ✔ |
| AUTH-04 | Admin and client roles. | Done ✔ |
| AUTH-05 | Limit features by role. | Done ✔: `ROLE_PERMISSIONS` in `app/security/permissions.py` |

## Products

| ID | Requirement | Status |
|---|---|---|
| PROD-01 | List and read products. | Done ✔ |
| PROD-02 | Create products. | Done ✔ |
| PROD-03 | Update products. | Done ✔ |
| PROD-04 | Delete products. | Done ✔ |
| PROD-05 | Sales and returns update the stock. | Done ✔ |

## Sales

| ID | Requirement | Status |
|---|---|---|
| CART-01 | Create carts. | Done ✔: the first `PUT /cart/items/{product_id}` creates it ([ADR-0007](adr/0007-one-pending-cart-per-user.md)) |
| CART-02 | Add, change and remove cart products. | Done ✔: `PUT` and `DELETE /cart/items/{product_id}` |
| CART-03 | Go back to carts that weren't finished. | Done ✔: the pending cart stays until checkout, `GET /cart` |
| SALE-01 | Turn a cart into a sale. | Done ✔: `POST /cart/checkout` |
| SALE-02 | A sale generates an invoice. | Done ✔: with cart, billing, payment and snapshots |
| SALE-03 | A sale reduces stock. | Done ✔ |
| SALE-04 | A sale asks for billing address and payment data. | Done ✔: no card data is stored ([ADR-0006](adr/0006-payment-data-handling.md)) |
| INV-01 | Get an invoice by its number. | Done ✔: `GET /invoices/{number}` |
| INV-02 | Returns restore stock. | Done ✔: `POST /invoices/{number}/returns` |

## Database

| ID | Requirement | Status |
|---|---|---|
| DB-01 | PostgreSQL. | Done ✔ |
| DB-02 | Entity-relationship diagram before building. | Done: ✔ [database.md](database.md) |
| DB-03 | Normalized tables. | Done: ✔ [database.md](database.md#normalization) |
| DB-04 | All database work goes through the ORM. | Done: ✔ SQLAlchemy and Alembic |

## Endpoints

| ID | Requirement | Status |
|---|---|---|
| API-01 | Read, create, update and delete endpoints for each relevant entity. Junction tables don't need them. | Done ✔, with two documented exceptions: invoices have no delete, they're cancelled with a return ([ADR-0005](adr/0005-invoice-snapshots-and-restricted-deletes.md)); the cart is created by its first item and emptied by removing its items ([ADR-0007](adr/0007-one-pending-cart-per-user.md)) |
| API-02 | Only admins create, update or delete products and invoices, and update or delete any user. Clients sign up through registration (AUTH-01). | Done ✔: admins create users with `POST /users` and change roles with `PATCH /users/{id}/role`, and the last admin can't be demoted or deleted ([ADR-0008](adr/0008-admins-manage-users-and-roles.md)). Invoices are updated with `PATCH /invoices/{number}` (billing only) and cancelled with a return instead of a delete ([ADR-0005](adr/0005-invoice-snapshots-and-restricted-deletes.md)). Clients create invoices only through checkout, which is a sale (API-03) |
| API-03 | Clients can use read endpoints, sales and carts. | Done ✔ |



## Caching

| ID | Requirement | Status |
|---|---|---|
| CACHE-01 | Decide which endpoints benefit from a cache. | Done ✔: products and invoices, see [caching.md](caching.md) |
| CACHE-02 | Every cache has invalidation conditions. | Done ✔ |
| CACHE-03 | Decide where a TTL is needed. | Done ✔: 5 min for single entries, 1 min for lists |

## Tests

| ID | Requirement | Status |
|---|---|---|
| TEST-01 | Unit tests with good coverage. | Done ✔: unit (passwords, tokens, permissions) and routes (auth, users, products, cart, checkout, invoices, returns, cache) |
| TEST-02 | Success and error cases, including messages. | Done ✔: the essential cases of every endpoint, listed in [testing.md](testing.md) |
| TEST-03 | A script runs the tests and writes a short report. | Done ✔: `python scripts/run_tests.py`, see [testing.md](testing.md#report-script-test-03) |
| TEST-04 | Documented steps to run the tests. | Done: ✔ [testing.md](testing.md) |

## Deliverables

| ID | Deliverable | Status |
|---|---|---|
| DEL-01 | Database diagrams | Done: ✔ [database.md](database.md) |
| DEL-02 | Reasons for technical decisions | Done: ✔ [adr/](adr/README.md), [caching.md](caching.md) |
| DEL-03 | README that explains how to run the server and database | Done ✔: [README.md](../README.md) |

