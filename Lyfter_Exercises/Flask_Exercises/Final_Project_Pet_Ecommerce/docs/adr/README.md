# Decisions

Each file records one technical decision and why it was made. If a decision changes after it's built, add a new file and mark the old one as superseded. Copy [0000-template.md](0000-template.md) for new ones.

| # | Decision | Built |
|---|---|---|
| [0001](0001-flask-sqlalchemy-layered-architecture.md) | Flask and SQLAlchemy in layers | Yes |
| [0002](0002-jwt-stateless-authentication.md) | JWT with RS256 and token version | Yes, except scrypt |
| [0003](0003-redis-cache-with-explicit-invalidation.md) | Redis with invalidation and TTL | Products only |
| [0004](0004-atomic-checkout-with-row-locking.md) | One transaction and row locks for checkout | Partly |
| [0005](0005-invoice-snapshots-and-restricted-deletes.md) | Invoice snapshots and restricted deletes | Partly |
| [0006](0006-payment-data-handling.md) | No sensitive payment data | No |
