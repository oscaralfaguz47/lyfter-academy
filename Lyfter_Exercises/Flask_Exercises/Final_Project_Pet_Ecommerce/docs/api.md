# API

Base URL: `http://localhost:5000/api/v1`

## Conventions

Every endpoint needs `Authorization: Bearer <access_token>`, except `/health`, `/auth/register`, `/auth/login` and `/auth/refresh-token`.

Successful responses wrap the result in `data`. Lists also return `meta`:

```json
{
  "data": [],
  "meta": { "page": 1, "per_page": 20, "total": 57, "total_pages": 3 }
}
```

- `POST` that creates something returns 201 and a `Location` header.
- `DELETE` returns 204 with no body.
- Lists accept `page` and `per_page` (100 at most).
- Money and quantities are strings (`"100.00"`, `"5.000"`), so clients don't lose precision.
- Dates are ISO 8601 in UTC.
- Unknown body fields return 422.

Errors use the format in [architecture.md](architecture.md#errors).

## Permissions

Own = allowed only on your own data. Someone else's returns 404.

| Endpoint | Admin | Client |
|---|---|---|
| `POST /auth/register`, `/login`, `/refresh-token` | Public | Public |
| `GET /auth/me`, `POST /auth/logout` | Yes | Yes |
| `GET /users` | Yes | No |
| `GET /users/{id}`, `PATCH /users/{id}` | All | Own |
| `POST /users`, `DELETE /users/{id}` | Yes | No |
| `GET /login-history` | Yes | No |
| `GET /products`, `GET /products/{id}` | Yes | Yes |
| `POST /products`, `PATCH`, `DELETE`, `PATCH .../restock` | Yes | No |
| `POST /carts` | Yes | Yes |
| `GET /carts`, `GET /carts/{id}` | All | Own |
| Change a cart, its items, or check it out | Own | Own |
| `GET /invoices`, `GET /invoices/{number}` | All | Own |
| `PATCH /invoices/{number}` | Yes | No |
| `POST /invoices/{number}/returns` | Yes | No |
| `GET /invoices/{number}/returns` | All | Own |

Clients can't list `/users` because it has other people's personal data. They read and update their own account at `/users/{id}`; someone else's id returns 404, the same as an id that doesn't exist. `/auth/me` also returns their account. Only admins delete users.

An admin changing someone else's cart gets 403, not 404, because admins can see every cart.

Permissions are defined in `app/security/permissions.py`. `flask --app app permissions` prints the table.

## Health

`GET /health` is 200 with `{"status": "ok", "database": "ok", "cache": "ok"}`. `cache` can be `"unreachable"` and the API still works. If the database is down it returns 503.

## Auth

| Endpoint | Body | Response | Errors |
|---|---|---|---|
| `POST /auth/register` | `name`, `email`, `phone_number` (up to 20 chars), `password` (8 to 128 chars) | 201 `user` and tokens | 409 email taken, 422 |
| `POST /auth/login` | `email`, `password` | 200 tokens | 401, 422 |
| `POST /auth/refresh-token` | `refresh_token` | 200 tokens | 401 |
| `GET /auth/me` | | 200 user and `permissions` | 401 |
| `POST /auth/logout` | | 204 | 401 |

Tokens look like this:

```json
{ "access_token": "...", "refresh_token": "...", "token_type": "Bearer", "expires_in": 900 }
```

A `role` field on register returns 422. A wrong password and an unknown email return the same message, so nobody can find out which emails exist. Logout revokes every token of that user.

## Users

| Endpoint | Body | Response | Errors |
|---|---|---|---|
| `GET /users` | `sort`: `id`, `-id`, `name`, `-name` | 200 list | |
| `GET /users/{id}` | | 200 | 404 |
| `POST /users` | `name`, `email`, `phone_number`, `password`, `role` | 201 | 409, 422 |
| `PATCH /users/{id}` | any of `name`, `email`, `phone_number`, `role` | 200 | 404, 409, 422 |
| `DELETE /users/{id}` | | 204 | 404, 409 if the user has invoices or products |

## Login history

`GET /login-history?user_id=` returns `id`, `login_date`, `user_id`, `user_ip` and `success`. It's read-only because it's an audit log.

## Products

| Endpoint | Body | Response | Errors |
|---|---|---|---|
| `GET /products` | `search`, `sort` | 200 list | |
| `GET /products/{id}` | | 200 | 404 |
| `POST /products` | `name`, `price`, optional `entry_date` | 201, stock is 0 | 409 name taken, 422 |
| `PATCH /products/{id}` | any of `name`, `price`, `entry_date` | 200 | 404, 409, 422 |
| `PATCH /products/{id}/restock` | `stock` (quantity to add) | 200 | 404, 422 |
| `DELETE /products/{id}` | | 204 | 404, 409 if already sold |

Stock isn't editable through `PATCH /products/{id}`. It only changes through restock, sales and returns, so each change has a clear cause.

```json
{
  "id": 1, "name": "Dog food", "price": "100.00", "stock": "5.000",
  "entry_date": "2026-11-05", "created_by_id": 1, "updated_by_id": 1,
  "created_at": "2026-11-05T23:53:52Z", "updated_at": "2026-11-05T23:53:52Z"
}
```

## Carts

| Endpoint | Body | Response | Errors |
|---|---|---|---|
| `POST /carts` | | 201 | |
| `GET /carts` | `status`; `user_id` for admins | 200 list | |
| `GET /carts/{id}` | | 200 | 404 |
| `DELETE /carts/{id}` | | 204 | 404, 409 if completed |
| `POST /carts/{id}/items` | `product_id`, `quantity` | 200 cart | 404, 409 if completed, 422 |
| `PATCH /carts/{id}/items/{product_id}` | `quantity` | 200 cart | 404, 409, 422 |
| `DELETE /carts/{id}/items/{product_id}` | | 200 cart | 404, 409 |

`GET /carts?status=pending` is how a user goes back to unfinished carts. Adding a product already in the cart adds to its quantity. `PATCH` replaces it.

```json
{
  "id": 31,
  "user_id": 7,
  "status": "pending",
  "items": [
    { "product_id": 1, "product_name": "Dog food", "unit_price": "100.00", "quantity": "2.000", "line_total": "200.00" }
  ],
  "subtotal": "200.00",
  "created_at": "2026-11-05T23:53:52Z",
  "updated_at": "2026-11-05T23:53:52Z"
}
```

Cart prices are current product prices. The final price is fixed at checkout.

## Checkout

`POST /carts/{id}/checkout` returns 201 with the invoice and a `Location` header.

```json
{
  "billing_address": {
    "address": "200m north of the church",
    "city": "Zarcero",
    "province": "Alajuela",
    "postal_code": "21101"
  },
  "payment": { "method": "sinpe", "reference": "20261105123456" }
}
```

Limits: `address` up to 100 characters, `city` and `province` up to 60, `postal_code` exactly 5 digits, and `reference` up to 40. `method` is `sinpe` or `card`.

The invoice is created as `paid`. The API records a payment made elsewhere and doesn't verify it; `reference` lets an admin check it later. If a payment never arrived, the admin returns every line.

For `"method": "card"`, `reference` must be exactly the last 4 digits. Other card fields are rejected as unknown, so a CVV can't get in. See [ADR-0006](adr/0006-payment-data-handling.md).

| Status | When |
|---|---|
| 403 | An admin checking out someone else's cart |
| 404 | The cart doesn't exist or isn't yours |
| 409 | Already completed, or not enough stock (details in `errors.products`) |
| 422 | Invalid body, or empty cart |

## Invoices

| Endpoint | Body | Response | Errors |
|---|---|---|---|
| `GET /invoices` | `invoice_number`, `client_id` (admins), `sort` | 200 list | |
| `GET /invoices/{number}` | | 200 | 404 |
| `PATCH /invoices/{number}` | any `billing_*` field | 200 | 404, 422 |

There's no `POST /invoices`. Checkout is the only way to create one, so an invoice can't exist without its sale and stock change.

There's no `DELETE` either, so `DELETE /invoices/{number}` returns 405. An invoice is a financial record, so it's never deleted. To cancel a sale, return every line. See [ADR-0005](adr/0005-invoice-snapshots-and-restricted-deletes.md).

`status` is `paid` or `returned`. See [Returns](#returns).

Only the billing fields can be edited. Amounts, lines and payment data can't. Fix those with a return.

```json
{
  "id": 1,
  "invoice_number": 100,
  "client_id": 7,
  "cart_id": 31,
  "status": "paid",
  "total_amount": "200.00",
  "billing_address": "200m north of the church",
  "billing_city": "Zarcero",
  "billing_province": "Alajuela",
  "billing_postal_code": "21101",
  "payment_method": "sinpe",
  "payment_reference": "20261105123456",
  "created_at": "2026-11-05T23:53:53Z",
  "invoice_lines": [
    { "id": 1, "product_id": 1, "product_name": "Dog food", "quantity": "2.000", "price": "100.00", "total_amount": "200.00" }
  ]
}
```

## Returns

`POST /invoices/{number}/returns` is admin only and returns 201. `reason` is up to 100 characters and each `quantity` must be greater than 0.

```json
{ "reason": "Damaged packaging", "lines": [{ "invoice_line_id": 1, "quantity": "1" }] }
```

```json
{
  "id": 5,
  "invoice_number": 100,
  "reason": "Damaged packaging",
  "refund_amount": "100.00",
  "invoice_status": "paid",
  "lines": [{ "invoice_line_id": 1, "quantity": "1.000" }],
  "created_at": "2026-11-05T23:53:53Z"
}
```

The invoice stays `paid` until every line is fully returned. Then it becomes `returned`. Returning every line is also how a sale is cancelled.

| Status | When |
|---|---|
| 404 | The invoice doesn't exist |
| 409 | The invoice is already `returned`, or the quantity exceeds what's left to return |
| 422 | Invalid body, duplicate line, or a line from another invoice |

`GET /invoices/{number}/returns` lists the returns of an invoice.

Returns have no `PATCH` or `DELETE`. They're a financial record, and undoing one would have to move stock back again.
