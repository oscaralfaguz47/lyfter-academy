CREATE TABLE Users (
    Id INTEGER PRIMARY KEY,
    FullName TEXT NOT NULL, -- VARCHAR(80)
    Email TEXT UNIQUE NOT NULL, -- VARCHAR(80)
    RegistrationDate TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE Products(
    Id INTEGER PRIMARY KEY,
    Code TEXT UNIQUE NOT NULL, -- VARCHAR(20)
    Name TEXT NOT NULL,  -- VARCHAR(50)
    Price DECIMAL(18,2) NOT NULL,
    EntryDate TEXT NOT NULL DEFAULT (datetime('now')),
    Brand TEXT NOT NULL,  -- VARCHAR(50)
    StockAvailable INTEGER NOT NULL
);

CREATE TABLE Reviews(
    Id INTEGER PRIMARY KEY,
    ProductId INTEGER NOT NULL REFERENCES Products(Id),
    Comment TEXT NOT NULL,  -- VARCHAR(2000)
    Rating INTEGER NOT NULL CHECK (Rating BETWEEN 1 AND 5),
    ReviewDate TEXT NOT NULL DEFAULT (datetime('now')),
    UserId INTEGER NOT NULL REFERENCES Users(Id),
    UNIQUE(ProductId, UserId)   -- Only one review per user and product
);
-- Reviews Table / Create indexes for performance
CREATE INDEX IX_Reviews_UserId ON Reviews(UserId);
CREATE INDEX IX_Reviews_ProductId ON Reviews(ProductId);

CREATE TABLE Invoices(
    Id INTEGER PRIMARY KEY,
    InvoiceNumber TEXT UNIQUE NOT NULL,  -- VARCHAR(80)
    PurchaseDate TEXT NOT NULL DEFAULT(datetime('now')),
    TotalAmount DECIMAL(18,2) NOT NULL,
    UserId INTEGER NOT NULL REFERENCES Users(Id)
);
-- Invoices Table / Create indexes for performance
CREATE INDEX IX_Invoices_UserId ON Invoices(UserId);

CREATE TABLE ProductInvoice(
    Id INTEGER PRIMARY KEY,
    ProductId INTEGER NOT NULL REFERENCES Products(Id),
    InvoiceId INTEGER NOT NULL REFERENCES Invoices(Id),
    Quantity INTEGER NOT NULL,
    UnitPrice DECIMAL(18, 2) NOT NULL,
    TotalAmount DECIMAL(18, 2) NOT NULL
);
-- ProductInvoice Table / Create indexes for performance
CREATE INDEX IX_ProductInvoice_ProductId ON ProductInvoice(ProductId);
Create INDEX IX_ProductInvoice_InvoiceId ON ProductInvoice(InvoiceId);

CREATE TABLE ShoppingCart(
    Id INTEGER PRIMARY KEY,
    UserId INTEGER NOT NULL UNIQUE REFERENCES Users(Id)  -- One cart per user, no index is required because it is unique and it creates the index
);

CREATE TABLE ShoppingCartProduct(
    Id INTEGER PRIMARY KEY,
    ShoppingCartId INTEGER NOT NULL REFERENCES ShoppingCart(Id),
    ProductId INTEGER NOT NULL REFERENCES Products(Id),
    Quantity INTEGER NOT NULL,
    UNIQUE(ShoppingCartId, ProductId)    -- One product once per cart
);
-- ShoppingCartProduct Table / Create indexes for performance
CREATE INDEX IX_ShoppingCartProduct_ProductId ON ShoppingCartProduct(ProductId);  -- Only for ProductId because ShoppingCartId was defined for the UNIQUE

CREATE TABLE PaymentMethodTypes(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL  -- VARCHAR(30)
);

CREATE TABLE PaymentMethods(
    Id INTEGER PRIMARY KEY,
    MethodTypeId INTEGER NOT NULL REFERENCES PaymentMethodTypes(Id),
    BankName TEXT  -- VARCHAR(80)
);
-- PaymentMethods Table / Create indexes for performance
CREATE INDEX IX_PaymentMethods_MethodTypeId ON PaymentMethods(MethodTypeId);

CREATE TABLE InvoicePaymentMethod(
    Id INTEGER PRIMARY KEY NOT NULL,
    InvoiceId INTEGER NOT NULL REFERENCES Invoices(Id),
    PaymentMethodId INTEGER NOT NULL REFERENCES PaymentMethods(Id),
    PaidAmount DECIMAL(18, 2) NOT NULL,
    PaidAt TEXT NOT NULL DEFAULT (datetime('now'))
);
-- InvoicePaymentMethod Table / Create indexes for performance
CREATE INDEX IX_InvoicePaymentMethod_InvoiceId ON InvoicePaymentMethod(InvoiceId);
CREATE INDEX IX_InvoicePaymentMethod_PaymentMethodId ON InvoicePaymentMethod(PaymentMethodId);

ALTER TABLE Invoices ADD BuyerPhone TEXT NULL;  -- VARCHAR(20)

ALTER TABLE Invoices ADD CashierCode TEXT NOT NULL DEFAULT '';  -- VARCHAR(10)


