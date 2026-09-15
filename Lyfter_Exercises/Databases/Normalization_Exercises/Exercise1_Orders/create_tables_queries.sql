CREATE TABLE Customers(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Phone TEXT NOT NULL,
    CreationDate TEXT NOT NULL DEFAULT(datetime('now'))
);

CREATE TABLE CustomerAddresses(
    Id INTEGER PRIMARY KEY,
    CustomerId INTEGER NOT NULL REFERENCES Customers(Id),
    FullAddress TEXT NOT NULL
);

CREATE TABLE Items(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL UNIQUE,
    UnitPrice DECIMAL(18,2) NOT NULL,
    CreationDate TEXT NOT NULL DEFAULT(datetime('now'))
);

CREATE TABLE Orders(
    Id INTEGER PRIMARY KEY,
    CustomerId INTEGER NOT NULL REFERENCES Customers(Id),
    CustomerAddressId INTEGER NULL REFERENCES CustomerAddresses(Id),
    DeliveryTime TEXT NOT NULL
);

CREATE TABLE OrderItems(
    Id INTEGER PRIMARY KEY,
    OrderId INTEGER NOT NULL REFERENCES Orders(Id),
    ItemId INTEGER NOT NULL REFERENCES Items(Id),
    Quantity INTEGER NOT NULL,
    UnitPrice INTEGER NOT NULL,
    SpecialRequest TEXT NULL,
    UNIQUE(OrderId, ItemId)
);

-- Create indexes for performance
CREATE INDEX IX_CustomerAddresses_CustomerId ON CustomerAddresses(CustomerId);
CREATE INDEX IX_Orders_CustomerAddressId ON Orders(CustomerAddressId);
CREATE INDEX IX_Orders_CustomerId ON Orders(CustomerId);
CREATE INDEX IX_OrderItems_ItemId ON OrderItems(ItemId);
