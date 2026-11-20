# 0008: Admins manage users and roles, and there's always one admin

**Status:** Accepted. Built.
**Date:** 2026-11-20

## Context

Users could only be created through the public `POST /auth/register`, which always makes clients, and a role could only change with `flask promote-admin`. That left the users CRUD incomplete, and there was no way to take the admin role away from someone. An admin could also delete their own account even as the last admin, and then nobody could manage products or users without server access.

## Decision

- `POST /users` lets an admin create an account and pick its role. Public sign-ups still go through `/auth/register` and are always clients.
- `PATCH /users/{id}/role` lets an admin promote or demote a user. `role` is still rejected in `PATCH /users/{id}`, so a role only changes through an endpoint made for it.
- Demoting or deleting the last admin returns 409. The service locks every admin row (`SELECT ... FOR UPDATE`) before counting, so two requests that remove the last two admins at once can't both pass.
- `flask promote-admin` stays, to create the first admin.

## Alternatives

- **Keep roles out of the API:** safer, but an admin who should lose access stays admin until someone with server access runs a command.
- **Forbid deleting your own account:** blocks the obvious case, but not two admins deleting each other at once, and it also stops an admin from leaving when there are others.
- **Count admins without a lock:** two requests can both see two admins and leave none.

## Trade-offs

A stolen admin token can now create admins. Tokens last 15 minutes and logout revokes them, and that risk already existed for every admin action.
