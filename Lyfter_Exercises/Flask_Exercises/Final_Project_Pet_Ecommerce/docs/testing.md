# Testing

## Running the tests

First time only:

1. Install the dev dependencies: `pip install -r requirements-dev.txt`. It includes pytest.
2. Create the test database. Its name must end in `_test`, for example `pet_ecommerce_test`. The tests refuse to run otherwise.
3. If `DB_SCHEMA` is set, create the same schema in the test database, owned by the app user: `CREATE SCHEMA <name> AUTHORIZATION <user>;`. Tests reuse `DB_SCHEMA`; the separate database is what isolates them.
4. Set `TEST_DATABASE_URL` and `TEST_REDIS_URL` in `.env`. Use a Redis database other than 0, for example `/1`: tests flush it and refuse to run against 0.
5. Start Redis: `docker start redis-cache`.

Then, from the project root:

```bash
pytest                              # everything
pytest tests/unit                   # pure logic, no database or Redis needed
pytest tests/routes/test_auth.py    # one file
pytest -k login                     # by name
pytest -x                           # stop at the first failure
```

`pyproject.toml` sets `pythonpath = ["."]`, so plain `pytest` can `import app`.

## Report script (planned, TEST-03)

`scripts/run_tests.py`:

1. Runs `[sys.executable, "-m", "pytest", "--junitxml=reports/junit.xml"]` with `subprocess.run`.
2. Reads the XML with `xml.etree.ElementTree`. `root.find("testsuite")` has `tests`, `failures`, `errors`, `skipped` and `time`.
3. Finds failures: each `testcase` with a `failure` or `error` child.
4. Writes `reports/test-report.md` and prints the same summary.
5. Exits with pytest's return code.

Coverage isn't included because `pytest-cov` is a new dependency. Add it only if the course allows it.

## What kind of tests

The assignment asks for tests of the API, and most of the risk is in rules PostgreSQL enforces: `FOR UPDATE`, `CHECK`, unique constraints. A mock wouldn't catch those failures. So:

- **`tests/unit/`** tests pure logic with no database: `TokenService`, passwords, schemas, `Actor.can`.
- **`tests/routes/`** tests through the Flask test client against the test database and Redis.

## Setup

```
tests/
├── conftest.py      # shared by every test; empty for now
├── unit/            # pure logic, no fixtures with I/O
└── routes/
    ├── conftest.py  # app, database, Redis and auth fixtures
    ├── helpers.py   # request bodies and headers
    └── test_*.py
```

The fixtures that touch PostgreSQL and Redis live in `tests/routes/conftest.py`, so `tests/unit` runs without Docker.

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
| `client_headers`, `other_client_headers` | `Authorization` header for a registered client |
| `admin_headers` | Same, for a user whose role was changed to admin in the database |
| `product` | A product with stock, created through the API |
| `pending_cart` | A cart with one item |
| `paid_invoice` | An invoice created through a real checkout |

Building data through the API makes tests slower but keeps them honest, since they follow what a real client does.

## Writing a test

Name: `test_<action>_<condition>_<result>`.

- Build bodies with `helpers.py` (`registration_body(**overrides)`) and override only the field the test is about. Use `example.com` emails and fake phone numbers.
- Compare concrete values with `==` (lists, dicts, sets). `all()` or a computed bool shows `assert False` with no diff, and `all([])` is `True`.
- Check response fields with an allowlist: `set(user) == PUBLIC_USER_FIELDS`. A blocklist like `"password_hash" not in user` misses fields you didn't think of.
- Test limits at one past the boundary: 7-character password, 21-character phone.
- Don't assert that two tokens differ. `iat` and `exp` are in seconds, so two tokens issued in the same second are identical.
- Don't assert on timing. The login timing equalizer is covered by code review, not tests.

Check the result and not only the status. Error tests check `status`, `detail`, and that nothing changed:

```python
def test_checkout_without_stock_returns_409_and_saves_nothing(client, client_headers, cart_over_stock):
    response = client.post(f"/api/v1/carts/{cart_over_stock['id']}/checkout", json=CHECKOUT_BODY, headers=client_headers)

    assert response.status_code == 409
    body = response.get_json()
    assert body["detail"] == "Not enough stock."
    assert body["errors"]["products"][0]["product_id"] == cart_over_stock["items"][0]["product_id"]

    invoices = client.get("/api/v1/invoices", headers=client_headers).get_json()
    assert invoices["meta"]["total"] == 0
```

To test Redis being down, swap the cache for one pointing to a closed port. Restore it in `finally`, since `app` is shared:

```python
app.extensions["cache"] = Cache(Redis.from_url("redis://127.0.0.1:1/0", socket_connect_timeout=0.2, socket_timeout=0.2))
```

For the concurrency tests, start several `threading.Thread`, each calling the endpoint with its own `app.test_client()`. Each request gets its own session. Save the status codes and assert something like `sorted(codes) == [201, 409, 409, 409, 409]`.

## Test cases

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
| Admin creates a user with a role | 201 |
| Admin changes a role | Applies on the user's next request |
| Delete a user with no history | 204 |
| Delete a user with invoices | 409 |

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

### Carts

| Case | Expected |
|---|---|
| Create | 201, `pending`, no items |
| Add the same product twice | Quantity adds up |
| Change quantity | Replaced |
| Quantity 0 or negative | 422 |
| Unknown product | 404 |
| Remove an item | Gone from the cart |
| `GET /carts?status=pending` | Only your pending carts |
| Another client's cart | 404 |
| Admin reads another's cart | 200 |
| Admin changes another's cart | 403 |
| Change or delete a completed cart | 409 |

### Checkout

| Case | Expected |
|---|---|
| Valid | 201, invoice `paid`, cart `completed`, stock reduced exactly |
| Totals | Exact `Decimal` values |
| Later price change | The invoice keeps the old price and name |
| Empty cart | 422 |
| Missing address or payment | 422 |
| Card reference not 4 digits, or a full card number | 422 |
| Extra field like `cvv` | 422 |
| Not enough stock | 409 and nothing saved |
| Same cart twice in a row | Second is 409 |
| Five threads, same cart | One invoice |
| Five carts, one unit of stock | One sale, four 409s, stock 0 |

### Invoices and returns

| Case | Expected |
|---|---|
| Owner or admin reads by number | 200 |
| Another client | 404 |
| Client lists | Only their own, even when sending another `client_id` |
| Admin updates billing | 200 |
| Client updates billing | 403 |
| `DELETE /invoices/{number}` | 405 |
| Partial return | 201, stock restored, still `paid` |
| Return everything | `returned` |
| Return more than what's left | 409, counting earlier returns |
| Line from another invoice | 422 |
| Return on a `returned` invoice | 409 |
| Client creates a return | 403 |

### Cache

| Case | Expected |
|---|---|
| Second read of a product | Key exists in Redis, same response |
| Update, restock, checkout, return | The product's key is gone and lists show new data |
| New invoice | The next list includes it |
| Invoice key for a return or update | Gone |
| Cached invoice, another client asks | 404 |
| Two clients, same params | Each sees their own list |
| Keys have a TTL | `ttl` is positive and within the expected range |
| Redis down | Reads and writes still answer |
