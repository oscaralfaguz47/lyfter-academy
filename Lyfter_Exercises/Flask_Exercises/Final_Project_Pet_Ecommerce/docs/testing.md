# Testing

## Running the tests

First time only:

1. Install the dev dependencies: `pip install -r requirements-dev.txt`. It includes pytest.
2. Create the test database. Its name must end in `_test`, for example `pet_ecommerce_test`. The tests refuse to run otherwise.
3. If `DB_SCHEMA` is set, create the same schema in the test database, owned by the app user: `CREATE SCHEMA <name> AUTHORIZATION <user>;`. Tests reuse `DB_SCHEMA`; the separate database is what isolates them.
4. Set `TEST_DATABASE_URL` and `TEST_REDIS_URL` in `.env`. Use a Redis database other than 0, for example `/1`: tests flush it and refuse to run against 0.
5. Start Redis: `docker start pet-ecommerce-redis-cache` (created in the README's first-time setup).

Then, from the project root:

```bash
pytest                              # everything
pytest tests/unit                   # pure logic, no database or Redis needed
pytest tests/routes/test_auth.py    # one file
pytest -k login                     # by name
pytest -x                           # stop at the first failure
```

`pyproject.toml` sets `pythonpath = ["."]`, so plain `pytest` can `import app`.

## Report script (TEST-03)

The assignment asks for a script that runs the tests and writes a short report. From the project root:

```bash
python scripts/run_tests.py
```

It runs `pytest -rA` from the project root, prints the output and saves it in `reports/test-report.txt`. `-rA` adds a summary at the end with every test and its result (`PASSED`, `FAILED`, `ERROR`), followed by the totals, like `132 passed in 35.25s`. The script exits with pytest's return code: 0 if everything passed, so `python scripts/run_tests.py && git push` only pushes on green.

It only uses the standard library (`subprocess`, `sys`, `pathlib`). `reports/` is generated, so it isn't committed.

Coverage isn't included because `pytest-cov` is a new dependency, and the assignment limits the libraries to the ones seen in the course.

## What kind of tests

The assignment asks for tests of the API, and most of the risk is in rules PostgreSQL enforces: `FOR UPDATE`, `CHECK`, unique constraints. A mock wouldn't catch those failures. So:

- **`tests/unit/`** tests pure logic with no database: `TokenService`, passwords, schemas, `Actor.can`.
- **`tests/routes/`** tests through the Flask test client against the test database and Redis.

## Setup

```
tests/
├── conftest.py          # pytest_plugins: registers the modules in routes/fixtures/
├── unit/                # pure logic, no fixtures with I/O
└── routes/
    ├── conftest.py      # infrastructure: app, redis_client, clean_state, client, db_session
    ├── fixtures/        # data fixtures, one module per area
    │   ├── users.py     # registered_user, other_user, admin_user and their headers
    │   ├── products.py  # product, stocked_product
    │   └── cart.py      # cart_with_item, paid_invoice
    ├── helpers/         # plain functions and constants, imported explicitly
    │   ├── users.py     # registration_body, login_body, bearer, test emails
    │   ├── products.py  # product_body
    │   └── cart.py      # CART_URL, CHECKOUT_URL, item_url, checkout_body
    └── test_*.py
```

The fixtures that touch PostgreSQL and Redis live in `tests/routes/conftest.py`, so `tests/unit` runs without Docker.

The data fixtures live in `tests/routes/fixtures/` and are registered with `pytest_plugins` in `tests/conftest.py`. Pytest only accepts `pytest_plugins` in the top-level conftest, because a plugin applies to the whole run. So `tests/unit` can see these fixtures too, but can't use them: they need `client`, which only exists under `tests/routes`. Modules in `fixtures/` are imported on every run, so they only define functions and do nothing at import time.

Where a fixture goes: in the test file if only that file uses it, in `fixtures/<area>.py` if several route files do, and in `tests/routes/conftest.py` only if it's infrastructure. A new module in `fixtures/` must be added to `pytest_plugins`.

- `app` (session): `create_app("testing")`. Refuses to run unless the database name ends in `_test`. Runs `drop_all` + `create_all` at the start, so an interrupted run never leaves old tables behind.
- `redis_client` (session): the tests' own Redis client. Refuses db 0.
- `clean_state` (autouse): deletes every table, children first, and flushes Redis **before** each test. Cleaning before instead of after means a crashed test can't leak data into the next one.

Tests delete data instead of rolling back, because services call `commit()` and the concurrency tests need real commits across connections. `DELETE` instead of `TRUNCATE`, because `TRUNCATE` takes an `ACCESS EXCLUSIVE` lock and hangs if any connection is still open.

Sequences reset once per run (`drop_all`), not between tests. Never assert a specific id or invoice number.

`create_app("testing")` fails if `TEST_DATABASE_URL` is missing, so `drop_all` can't fall back to your development database. Don't point that variable at your development database either.

Fixtures:

| Fixture | Gives you |
|---|---|
| `client` | Flask test client, new for each test |
| `registered_user` | `data` from `POST /auth/register`: `user` plus tokens |
| `db_session` | A session to check side effects the API doesn't show, like login history. Never use it to create data |
| `redis_client` | Raw Redis client, for checking keys and TTLs |
| `other_user` | A second registered client. Use it for "someone else's" cases |
| `admin_user` | A registered user promoted with `flask promote-admin`, the same way the first admin is created in production. Its `user.role` still says `client`, because the data was captured before the promotion |
| `client_headers`, `other_client_headers`, `admin_headers` | `Authorization` header for `registered_user`, `other_user` and `admin_user` |
| `product` | A product created by `admin_user` through the API, from `product_body()`. Stock starts at 0 |
| `stocked_product` | `product` with 10 units added through `PATCH /products/{id}/restock`. Use it for cart and checkout tests, because `PUT /cart/items` rejects a quantity over the stock |
| `cart_with_item` | `registered_user`'s cart with 2 units of `stocked_product`, through `PUT /cart/items` |
| `paid_invoice` | The invoice from checking out `cart_with_item` with `checkout_body()`, through `POST /cart/checkout` |

Building data through the API makes tests slower but keeps them honest, since they follow what a real client does.

## Writing a test

Name: `test_<action>_<condition>_<result>`.

- Build bodies with the builders in `helpers/` (`registration_body(**overrides)`, `product_body(**overrides)`) and override only the field the test is about. Import them from their module, like `from tests.routes.helpers.users import registration_body`. Use `example.com` emails and fake phone numbers.
- Compare concrete values with `==` (lists, dicts, sets). `all()` or a computed bool shows `assert False` with no diff, and `all([])` is `True`.
- Check response fields with an allowlist: `set(user) == PUBLIC_USER_FIELDS`. A blocklist like `"password_hash" not in user` misses fields you didn't think of.
- Test limits at one past the boundary: 7-character password, 21-character phone.
- Don't assert that two tokens differ. `iat` and `exp` are in seconds, so two tokens issued in the same second are identical.
- Don't assert on timing. The login timing equalizer is covered by code review, not tests.

Check the result and not only the status. Error tests check `status`, `detail`, and that nothing changed:

```python
def test_checkout_without_stock_returns_409_and_saves_nothing(client, client_headers, cart_over_stock):
    response = client.post("/api/v1/cart/checkout", json=CHECKOUT_BODY, headers=client_headers)

    assert response.status_code == 409
    body = response.get_json()
    assert body["detail"] == "Not enough stock."
    assert body["errors"]["products"][0]["product_id"] == cart_over_stock["cart_items"][0]["product"]["id"]

    invoices = client.get("/api/v1/invoices", headers=client_headers).get_json()
    assert invoices["meta"]["total"] == 0
```

## Test cases

Each table lists what the tests cover. The cart, checkout, invoice and cache tests stick to the essential cases on purpose: the goal is to cover the main flow and its expected failures, not every combination.

### Auth and permissions

| Case | Expected |
|---|---|
| Register with valid data | 201, role `client`, no password in the response |
| Register with an existing email | 409 |
| Register with a bad email, short password, no `phone_number` or a `role` field | 422 with `errors` per field |
| Login with valid data | 200 and tokens, attempt saved in history |
| Wrong password and unknown email | 401, same `detail` in both |
| No token, expired, tampered | 401 and `WWW-Authenticate: Bearer` |
| Refresh token used as access token | 401 |
| Valid refresh | 200, new tokens |
| Logout, then use the old token | 401 |
| Client calls each admin endpoint (parametrize) | 403 |
| Password stored | Not the plain text, verifies correctly, two hashes of the same password differ |

### Users

| Case | Expected |
|---|---|
| User promoted with `flask promote-admin` | Admin access on the next request, with the same token |
| Client or admin sends `role` in `PATCH /users/{id}` | 422, role unchanged |
| Client reads or updates their own account | 200, change saved |
| Client reads or updates another user | 404, same `detail` as an unknown id, nothing changed |
| Client deletes their own account | 403 |
| Delete a user with no history | 204 |
| Delete a user with invoices | 409 |
| Admin creates a user with a role | 201, `Location`, and the new user can log in |
| Client creates a user | 403 |
| Admin demotes another admin | 200 |
| Demote or delete the last admin | 409, nothing changed |

### Products

| Case | Expected |
|---|---|
| Client lists and reads | 200 |
| Admin creates | 201, stock 0, `Location` header |
| Duplicate name | 409 |
| Price 0, negative or with 3 decimals | 422 |
| Unknown product | 404 with its id in `detail` |
| Restock | Stock increases |
| Delete with no sales | 204, removed from carts that had it |
| Delete after a sale | 409 |

### Cart

In `tests/routes/test_cart.py`:

| Case | Expected |
|---|---|
| `GET /cart` with no cart | 200, no items, total `"0.00"` |
| First `PUT` | 200, the item with its total, and `GET /cart` shows the same |
| `PUT` the same product again | Quantity replaced, not added |
| Quantity over the stock | 409 with `errors.products`, and the cart stays empty |
| Quantity 0, negative or with 4 decimals | 422 on `quantity` |
| Remove an item twice | 200 without it, then 404 |
| Another user | Can't see or remove your items |

### Checkout

In `tests/routes/test_checkout.py`:

| Case | Expected |
|---|---|
| Valid | 201, `Location` header, invoice `paid` with its line, billing and payment; stock reduced and `GET /cart` empty |
| No cart | 409 |
| Not enough stock (another user bought it first) | 409 with `errors.products`, no invoice, the cart keeps its item |
| Full card number as `reference` | 422 on `payment`, and the cart keeps its item |
| Same cart twice | Second is 409 |

Concurrency tests (several threads checking out at once) aren't included. The row locks were checked by hand with two real connections.

### Invoices and returns

In `tests/routes/test_invoices.py`:

| Case | Expected |
|---|---|
| Owner reads by number | 200, the same invoice checkout returned |
| Another client reads it | 404 |
| Admin updates the billing city | 200, only the city changed |
| Client updates the billing | 403, nothing changed |
| Partial return | 201, refund at the invoice price, stock restored, still `paid` |
| Return everything | `returned` |
| Return more than what's left, counting an earlier return | 409 with `errors.lines` |
| Client creates a return | 403 |

### Cache

In `tests/routes/test_cache.py`:

| Case | Expected |
|---|---|
| Read an invoice twice | The key exists in Redis with a TTL, and both reads are the same |
| Cached invoice, another client asks | 404 |
| Two clients, same params | Each sees their own list |
| Return on a cached invoice | The next read shows `returned` |
| Invalidate with no keys | The list version still goes up |
