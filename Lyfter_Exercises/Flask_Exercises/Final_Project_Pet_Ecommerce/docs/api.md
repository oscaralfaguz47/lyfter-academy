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
| `DELETE /users/{id}` | Yes | No |
| `GET /login-history` | Yes | No |
| `GET /products`, `GET /products/{id}` | Yes | Yes |
| `POST /products`, `PATCH`, `DELETE`, `PATCH .../restock` | Yes | No |
| `GET /cart`, `PUT` and `DELETE /cart/items/{product_id}`, `POST /cart/checkout` | Own | Own |
| `GET /invoices`, `GET /invoices/{number}` | All | Own |
| `PATCH /invoices/{number}` (not built yet) | Yes | No |
| `POST /invoices/{number}/returns` | Yes | No |
| `GET /invoices/{number}/returns` | All | Own |

Clients can't list `/users` because it has other people's personal data. They read and update their own account at `/users/{id}`; someone else's id returns 404, the same as an id that doesn't exist. `/auth/me` also returns their account. Only admins delete users.

New accounts are always clients. The API can't change a role: a `role` field in `PATCH /users/{id}` returns 422, even for admins. Only the server operator promotes a user, with `flask promote-admin <email>`.

`/cart` is always the cart of the user in the token, for admins too. There's no cart id in the URL, so nobody can reach someone else's cart. See [ADR-0007](adr/0007-one-pending-cart-per-user.md).

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
| `PATCH /users/{id}` | any of `name`, `email`, `phone_number` | 200 | 404, 409, 422 |
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

## Cart

Each user has one pending cart, always at `/cart`. See [ADR-0007](adr/0007-one-pending-cart-per-user.md).

| Endpoint | Body | Response | Errors |
|---|---|---|---|
| `GET /cart` | | 200 cart, empty if there's none | |
| `PUT /cart/items/{product_id}` | `quantity` (greater than 0, up to 3 decimals) | 200 cart | 404 product not found, 409 not enough stock (details in `errors.products`), 422 |
| `DELETE /cart/items/{product_id}` | | 200 cart | 404 the product isn't in the cart |

There's no `POST /cart`. The first `PUT` creates the cart, and `GET /cart` never creates it. `PUT` sets the quantity, it doesn't add to it, so sending the same request twice leaves the same cart. `product_id` goes only in the URL: in the body it returns 422.

Removing the last item leaves an empty pending cart, and the next `PUT` reuses it. The pending cart stays until it's checked out, so `GET /cart` is how a user goes back to an unfinished cart.

```json
{
  "cart_items": [
    { "product": { "id": 1, "name": "Dog food", "price": "10.35" }, "quantity": "2.000", "total_amount": "20.70" }
  ],
  "total_amount": "20.70"
}
```

Cart prices are current product prices. The final price is fixed at checkout. The stock check in `PUT` is only early feedback: stock isn't reserved, and checkout checks it again with a lock.

## Checkout

`POST /cart/checkout` buys every item in the user's pending cart. It returns 201 with the invoice and a `Location` header to `/invoices/{number}`. The cart becomes `completed`.

```json
{
  "billing": {
    "address": "200m north of the church",
    "city": "Zarcero",
    "province": "Alajuela",
    "postal_code": "21101"
  },
  "payment": { "method": "sinpe", "reference": "20261105123456" }
}
```

Limits: `address` 1 to 100 characters, `city` and `province` 1 to 60, `postal_code` 1 to 5, and `reference` 1 to 40. `method` is `sinpe` or `card`.

The invoice is created as `paid`. The API records a payment made elsewhere and doesn't verify it; `reference` lets an admin check it later. If a payment never arrived, the admin returns every line.

For `"method": "card"`, `reference` must be exactly the last 4 digits. Other card fields are rejected as unknown, so a CVV can't get in. See [ADR-0006](adr/0006-payment-data-handling.md).

| Status | When |
|---|---|
| 401 | No valid token |
| 409 | The cart is empty or doesn't exist, or there's not enough stock (details in `errors.products`) |
| 422 | Invalid body |

Checking out the same cart twice returns 409 the second time: the cart is already `completed`, so the user has no pending cart.

## Invoices

| Endpoint | Body | Response | Errors |
|---|---|---|---|
| `GET /invoices` | `invoice_number`, `client_id` (admins), `sort` | 200 list | |
| `GET /invoices/{number}` | | 200 | 404, also for someone else's invoice |
| `PATCH /invoices/{number}` (not built yet) | any `billing` field | 200 | 404, 422 |

`{number}` is the `invoice_number` printed on the invoice (it starts at 100), not the internal `id`.

There's no `POST /invoices`. `POST /cart/checkout` is the only way to create one, so an invoice can't exist without its cart, sale and stock change.

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
  "created_at": "2026-11-05T23:53:53Z",
  "invoice_lines": [
    { "id": 1, "product_id": 1, "product_name": "Dog food", "quantity": "2.000", "price": "100.00", "total_amount": "200.00" }
  ],
  "billing": {
    "address": "200m north of the church",
    "city": "Zarcero",
    "province": "Alajuela",
    "postal_code": "21101"
  },
  "payment": { "method": "sinpe", "reference": "20261105123456" }
}
```

`billing` and `payment` come out grouped, with the same shape as the checkout body. In the database they're the `billing_*` and `payment_*` columns. `product_name` and `price` are the values at the time of the sale ([ADR-0005](adr/0005-invoice-snapshots-and-restricted-deletes.md)). The line `id` is what a return uses as `invoice_line_id`.

## Returns

`POST /invoices/{number}/returns` is admin only and returns 201, with a `Location` header to `GET /invoices/{number}/returns`. `reason` is 1 to 100 characters, and each `quantity` must be greater than 0. `invoice_line_id` is the `id` of a line in the invoice response.

```json
{ "reason": "Damaged packaging", "lines": [{ "invoice_line_id": 1, "quantity": "1" }] }
```

```json
{
  "id": 5,
  "reason": "Damaged packaging",
  "refund_amount": "100.00",
  "created_at": "2026-11-05T23:53:53Z",
  "invoice_return_lines": [{ "invoice_line_id": 1, "quantity": "1.000" }],
  "invoice_number": 100,
  "invoice_status": "paid"
}
```

The refund uses the price frozen in the invoice line, not today's product price. The returned quantity goes back to stock. The invoice stays `paid` until every line is fully returned, counting earlier returns. Then it becomes `returned`. Returning every line is also how a sale is cancelled.

| Status | When |
|---|---|
| 403 | A client creating a return |
| 404 | The invoice doesn't exist |
| 409 | The invoice is already `returned`, or a quantity exceeds what's left to return (details in `errors.lines`) |
| 422 | Invalid body, the same line twice, or a line from another invoice |

`GET /invoices/{number}/returns` lists the returns of an invoice, oldest first. The owner and admins can read it; someone else's invoice returns 404.

Returns have no `PATCH` or `DELETE`. They're a financial record, and undoing one would have to move stock back again.
