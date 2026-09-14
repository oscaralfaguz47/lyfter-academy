## ORDERS TABLE

**Notes:**
    - I decided to create the table Customers because the Orders table totally requires it to centralize the customer information such as Name, Phone, Address, or other future fields that it could have. Imagine we have millions of orders, we are going to consume a lot of bytes and we have to enter all the clients name every single time an order is created.
    - For Items, is better to have only the ItemId in the Orders table than the ItemId and the ItemName, if you enter manually the item name, the queries will not be exact and are going to be less efficient.
    - I created the OrderSpecialRequests table because it's easier to handle customs special requests than enter the request every single time in a new order.
    - Now the new created tables are opened for future changes like adding more columns for customization and son on.