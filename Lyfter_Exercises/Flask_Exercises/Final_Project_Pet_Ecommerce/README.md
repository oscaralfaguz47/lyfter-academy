# Pet E-commerce API

Backend for a pet products store: users and roles, products and stock, carts, checkout with invoices, returns, and a Redis cache. Built with Flask, SQLAlchemy, PostgreSQL and Redis.

The design and every technical decision are in [`docs/`](#documentation).

## Requirements

- Python 3.14
- PostgreSQL
- Docker, to run Redis
- OpenSSL, to create the JWT keys

## First time setup

Run every command from the project root.

1. Create and activate a virtual environment. Activate it again in every new terminal.

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the dependencies. `requirements-dev.txt` includes the app's and pytest.

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements-dev.txt
   ```

3. Create your `.env` from the template and fill in the values. Never commit `.env`.

   ```bash
   cp .env.example .env
   ```

   | Variable | What it is |
   |---|---|
   | `APP_ENV` | `development`, `testing` or `production` |
   | `SECRET_KEY` | Flask secret key |
   | `DATABASE_URL` | PostgreSQL URL of the development database |
   | `DB_SCHEMA` | Optional PostgreSQL schema. Leave it empty to use `public` |
   | `REDIS_URL` | Redis URL, for example `redis://127.0.0.1:6379/0` |
   | `LOG_LEVEL` | For example `INFO` |
   | `JWT_PRIVATE_KEY_PATH`, `JWT_PUBLIC_KEY_PATH` | The key files from step 4 |
   | `JWT_ACCESS_TOKEN_MINUTES`, `JWT_REFRESH_TOKEN_DAYS` | Token lifetimes |
   | `TEST_DATABASE_URL`, `TEST_REDIS_URL` | Only for tests, see [testing.md](docs/testing.md) |

   The app stops at startup if a required variable is missing.

4. Create the RSA key pair that signs the JWTs. `keys/` is ignored by git.

   ```bash
   mkdir -p keys
   openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out keys/jwt_private.pem
   openssl rsa -in keys/jwt_private.pem -pubout -out keys/jwt_public.pem
   ```

5. Create the PostgreSQL database named in `DATABASE_URL`, for example:

   ```bash
   createdb pet_ecommerce
   ```

6. Create the Redis container. Docker must be running.

   ```bash
   docker run -d --name pet-ecommerce-redis-cache -p 127.0.0.1:6379:6379 redis:8-alpine \
     redis-server --save "" --appendonly no --maxmemory 128mb --maxmemory-policy volatile-lru
   ```

   `volatile-lru` only evicts keys with a TTL, so the cache's version counters are never lost. See [caching.md](docs/caching.md).

7. Create the tables.

   ```bash
   python -m db.init_db
   ```

   On an empty database this creates every table through the ORM and marks Alembic at the latest migration. The migrations in `db/migrations/` start after the first tables were created, so `alembic upgrade head` alone can't build a database from scratch. Don't run `alembic init`: Alembic is already set up.

8. Start the API.

   ```bash
   flask --app app run --debug
   ```

   It listens on `http://localhost:5000/api/v1`. Check it with:

   ```bash
   curl http://localhost:5000/api/v1/health
   ```

   `{"status": "ok", "database": "ok", "cache": "ok"}` means PostgreSQL and Redis are reachable.

9. Create the first admin. Register a user with `POST /api/v1/auth/register`, then promote it. The API can't change roles, on purpose.

   ```bash
   flask --app app promote-admin <the user's email>
   ```

## Every day

```bash
source .venv/bin/activate
docker start pet-ecommerce-redis-cache
alembic upgrade head          # apply new migrations, if there are any
flask --app app run --debug
```

## Changing the database

1. Change the models in `app/models/`. A new model must be imported in `app/models/__init__.py`, or Alembic won't see it.
2. Generate the migration:

   ```bash
   alembic revision --autogenerate -m "describe the change"
   ```

3. Open the file in `db/migrations/versions/` and review it before applying it. Autogenerate doesn't detect a new `CheckConstraint` on an existing table: add it by hand with `op.create_check_constraint`.
4. Apply it:

   ```bash
   alembic upgrade head
   ```

## Tests

The tests need their own PostgreSQL database, whose name must end in `_test`, and a Redis database other than 0. They refuse to run otherwise, so they can't wipe your development data. The full setup is in [testing.md](docs/testing.md).

Run them and write the report:

```bash
python scripts/run_tests.py
```

It prints the results and saves them in `reports/test-report.txt`. It exits with pytest's code, so it fails if any test fails.

To run only some tests:

```bash
pytest tests/routes/test_cart.py                    # one file
pytest tests/routes/test_cart.py::test_get_cart_without_cart_returns_empty_cart   # one test
pytest -k checkout                                  # by name
```

## Useful commands

```bash
flask --app app permissions                         # roles and their permissions
docker exec -it pet-ecommerce-redis-cache redis-cli MONITOR   # every command Redis receives
```

## Documentation

| Document | What's in it |
|---|---|
| [api.md](docs/api.md) | Every endpoint, its body, responses, errors and permissions |
| [architecture.md](docs/architecture.md) | Layers, errors, cart states, checkout and returns step by step |
| [database.md](docs/database.md) | Tables, constraints, entity-relationship diagram, normalization and deletes |
| [caching.md](docs/caching.md) | What's cached and why, invalidation and TTLs |
| [testing.md](docs/testing.md) | Test setup, fixtures and the cases covered |
| [requirements.md](docs/requirements.md) | Each requirement of the assignment and its status |
| [adr/](docs/adr/README.md) | One file per technical decision and its reasons |
