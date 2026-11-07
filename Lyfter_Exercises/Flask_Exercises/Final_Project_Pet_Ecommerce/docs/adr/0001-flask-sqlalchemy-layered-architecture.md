# 0001: Flask and SQLAlchemy in layers

**Status:** Accepted
**Date:** 2026-11-05

## Context

The assignment requires Flask, PostgreSQL and an ORM for all database work. Checkout and returns are the riskiest parts and need to be testable.

## Decision

SQLAlchemy 2 as the ORM, Alembic for migrations and Pydantic for validation. The code runs in layers: routes, services, repositories, models. Services commit, repositories flush.

## Alternatives

- **Everything in the routes:** faster at first, but HTTP and business rules get mixed and files grow quickly.
- **Raw SQL:** the assignment forbids it (ORM only).
- **Hexagonal architecture:** cleaner boundaries, but this project has one database and no need to swap it. The extra interfaces wouldn't pay off.
- **`create_all` only:** can't change tables that already exist. `db/init_db.py` keeps it for a first setup and then stamps Alembic.

## Trade-offs

More files per feature. Adding one means touching a schema, repository, service and route, but each file does one thing.

Services receive the SQLAlchemy `Session` directly, so they aren't fully isolated from the ORM. It's a fair price at this size.
