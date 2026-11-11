# Requirements


## Users and authentication

| ID | Requirement | Status |
|---|---|---|
| AUTH-01 | Register. New accounts are clients. | Done ✔|
| AUTH-02 | Log in and receive tokens. | Done ✔ |
| AUTH-03 | Validate the token on every request to other modules. | Done ✔ |
| AUTH-04 | Admin and client roles. | Done ✔ |
| AUTH-05 | Limit features by role. | Partial ⏳ |

## Products

| ID | Requirement | Status |
|---|---|---|
| PROD-01 | List and read products. | Partial: clients get 403 ⏳ |
| PROD-02 | Create products. | Done ✔ |
| PROD-03 | Update products. | Done ✔ |
| PROD-04 | Delete products. | Done ✔ |
| PROD-05 | Sales and returns update the stock. | Partial: sales only ⏳ |

## Sales

| ID | Requirement | Status |
|---|---|---|
| CART-01 | Create carts. | Missing ⏳ |
| CART-02 | Add, change and remove cart products. | Missing ⏳ |
| CART-03 | Go back to carts that weren't finished. | Missing ⏳ |
| SALE-01 | Turn a cart into a sale. | Missing: ⏳ `POST /invoices` buys without a cart |
| SALE-02 | A sale generates an invoice. | Partial, needs the new fields ⏳ |
| SALE-03 | A sale reduces stock. | Done ✔ |
| SALE-04 | A sale asks for billing address and payment data. | Missing ⏳ |
| INV-01 | Get an invoice by its number. | Partial: ⏳ uses the internal id |
| INV-02 | Returns restore stock. | Missing ⏳ |

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
| API-01 | Read, create, update and delete endpoints for each relevant entity. Junction tables don't need them. | Partial ⏳. Invoices have no delete on purpose, see [ADR-0005](adr/0005-invoice-snapshots-and-restricted-deletes.md) |
| API-02 | Only admins create, update or delete products and invoices, and update or delete any user. Users are created only through registration (AUTH-01); admins are promoted with `flask promote-admin`. | Partial: ⏳ invoice update is missing. Invoices are cancelled with a return instead of a delete ([ADR-0005](adr/0005-invoice-snapshots-and-restricted-deletes.md)). Clients create invoices only through checkout, which is a sale (API-03) |
| API-03 | Clients can use read endpoints, sales and carts. | Partial ⏳ |



## Caching

| ID | Requirement | Status |
|---|---|---|
| CACHE-01 | Decide which endpoints benefit from a cache. | Partial: ⏳ products only |
| CACHE-02 | Every cache has invalidation conditions. | Partial: ⏳ products only |
| CACHE-03 | Decide where a TTL is needed. | Partial: ⏳ products only |

## Tests

| ID | Requirement | Status |
|---|---|---|
| TEST-01 | Unit tests with good coverage. | In progress: passwords, auth, permissions |
| TEST-02 | Success and error cases, including messages. | In progress: auth, permissions, own account |
| TEST-03 | A script runs the tests and writes a short report. | Missing ⏳ |
| TEST-04 | Documented steps to run the tests. | Done: ✔ [testing.md](testing.md) |

## Deliverables

| ID | Deliverable | Status |
|---|---|---|
| DEL-01 | Database diagrams | Done: ✔ [database.md](database.md) |
| DEL-02 | Reasons for technical decisions | Done: ✔ [adr/](adr/README.md), [caching.md](caching.md) |
| DEL-03 | README that explains how to run the server and database | Partial: ⏳ it needs to be updated as I'm programming |
| DEL-04 | Tests in the same PR, ready to run | Missing ⏳ |
| DEL-05 | Code delivered through a GitHub PR | Missing ⏳ |

