# 0006: No sensitive payment data

**Status:** Accepted, not built yet.
**Date:** 2026-11-05

## Context

The assignment asks for payment data at checkout. The business takes SINPE today. Storing card numbers would bring PCI DSS requirements and a serious risk if data leaks. This API doesn't charge anyone: it records a payment made elsewhere.

## Decision

Store only `payment_method` and `payment_reference`.

- `sinpe`: the transaction number, 1 to 40 characters.
- `card`: exactly the last 4 digits. Anything else returns 422, including a full card number.

`InputSchema` rejects unknown fields, so `cvv` or `expiry` return 422 without extra code. Validate the reference in a `model_validator` on `PaymentDetails`, the same way `PurchaseRequest` checks for duplicates.

Don't log payment data.

## Alternatives

- **Encrypted card data:** still in PCI scope and needs key management, for data the API doesn't use.
- **A payment gateway:** the right choice for real online payments, but out of scope here.

## Trade-offs

The API trusts that the payment happened. The reference allows checking it later against SINPE or card statements.
