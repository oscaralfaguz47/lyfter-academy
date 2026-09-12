## REFLECTIVE QUESTIONS

**Users Table:**
    *1.*Must every invoice be linked to a user, or can an invoice exist without an account?
        Every invoice should have a linked account (UserId). But what's going to happen with a user that wants to buy as a guest without creating an account?, the logic behind the scenes in the backend would be: with the email that the user provides while making the purchase it will be used to create the account, even we can take the name of the user from the checkout form.
    *2.*Do we need an intermediate table?
        No, we don't. The user can have multiple invoices, but an invoice cannot belong to multiple users. In my case what I did was to implement the UserId in the Invoices table as non-nullable. 
    *3.*Is it necessary to keep the BuyerEmail as we did in the previous exercise?
        No, it's not necessary, by implementing the new Users table, we can take the email that in this case is going to the same as the BuyerEmail.

**Reviews Table**
    *1.*Could a review exist without a product or user?
        Case without a user: No, it couldn't, as we create the user account even if the user is a guest, we already have the UserId related to the provided email, but I would make some improvements for example: If the user is going to create a review as a guest, the app is going to ask them for the email which they made the purchase and select the product (only if the user already made a purchase), if the user doesn't have a purchase yet show a message something like: "Make a purchase to leave a review and let us know your thoughts about the product"

        Case without a product: It depends on the company's business logic. In my case I prefer to let the ProductId as non-nullable to force the user to leave a review only if they made a purchase of the product, just to avoid people making fake bad reviews even if they don't made a purchase yet. If you want to let the logged in users to leave other reviews for example: the service, the support, etc, you must change the ProductId as nullable and probably create a second table as "Review Category" and add a ReviewCategoryId column in Reviews table to separate a little bit more the reviews.

**Payment Methods Table**
    *1.*Do every invoice should have a payment method or they can have more than one?
        We cannot use only one payment method for an invoice, because what are we going to do if a client wants to pay the invoice partially with a transfer and the other part by credit card?, We totally need to implement a second table something like: InvoicePaymentMethod to let the user use multiple payment methods for one invoice.