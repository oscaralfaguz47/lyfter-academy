# 0002: JWT with RS256 and token version

**Status:** Accepted. Replacing MD5 with scrypt is still pending.
**Date:** 2026-11-05

## Context

Every request to products and sales needs a valid identity and role. Logging out has to work, and plain JWTs can't be revoked.

## Decision

- Access tokens last 15 minutes and refresh tokens 7 days, signed with RS256.
- Claims: `sub`, `type`, `ver`, `iat`, `exp`. The role isn't in the token.
- Each request loads the user and compares `ver` with `users.token_version`. Logout increments it, which revokes every token that user has.
- Passwords use scrypt from `hashlib`.
- Permissions are checked by name (`products:create`), not by role. `ROLE_PERMISSIONS` is the only place that links them.

## Alternatives

- **Flask sessions:** need cookies and CSRF protection, which don't fit API clients as well.
- **HS256:** simpler, but anyone able to verify tokens could also sign them.
- **Role in the token:** avoids a query, but a role change would wait until the token expires.
- **Token blacklist in Redis:** would make security depend on the cache, which is allowed to fail.
- **bcrypt or Argon2:** both good, but they're new dependencies. scrypt is in the standard library.

## Trade-offs

One indexed query per request, in exchange for immediate logout and role changes. Logout closes every device, not just the current one. Refresh tokens aren't rotated, so a stolen one stays usable for up to 7 days or until logout.
