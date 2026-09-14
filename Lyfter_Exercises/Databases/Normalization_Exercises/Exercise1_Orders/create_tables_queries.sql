CREATE TABLE Customers(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Phone TEXT NOT NULL,
    Address TEXT NOT NULL,
    CreationDate TEXT NOT NULL DEFAULT(datetime('now'))
);

CREATE TABLE Items(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL UNIQUE,
    CreationDate TEXT NOT NULL DEFAULT(datetime('now'))
);

CREATE TABLE OrderSpecialRequests(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL UNIQUE,
    CreationDate TEXT NOT NULL DEFAULT(datetime('now'))
);

CREATE TABLE Orders(
    Id INTEGER PRIMARY KEY,
    CustomerId INTEGER NOT NULL REFERENCES Customers(Id),
    ItemId INTEGER NOT NULL REFERENCES Items(Id),
    Price DECIMAL(18, 2) NOT NULL,
    Quantity INTEGER NOT NULL,
    SpecialRequestId INTEGER NOT NULL REFERENCES OrderSpecialRequests(Id),
    Delivery TEXT NOT NULL
);

-- Create indexes for performance
CREATE INDEX IX_Orders_CustomerId ON Orders(CustomerId);
CREATE INDEX IX_Orders_ItemId ON Orders(ItemId);
CREATE INDEX IX_Orders_SpecialRequestId ON Orders(SpecialRequestId);