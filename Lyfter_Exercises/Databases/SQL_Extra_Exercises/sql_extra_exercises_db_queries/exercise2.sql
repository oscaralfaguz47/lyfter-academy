-- EXERCISE 2

-- Insert 10 rows in Products with ProductName, Price and StockAvailable
INSERT INTO Products (Code, Name, Price, Brand, StockAvailable, CategoryId) VALUES
('PR0007', 'Elantra', 35000, 'Hyundai', 8, (SELECT Id FROM Categories WHERE Name = 'Vehicles')),
('PR0008', 'Tucson', 40000, 'Hyundai', 3, (SELECT Id FROM Categories WHERE Name = 'Vehicles')),
('PR0009', 'Sock absorber', 200, 'Toyota', 25, (SELECT Id FROM Categories WHERE Name = 'Vehicle parts and accessories')),
('PR0010', 'Samsung Galaxy S24 FE', 600, 'Samsung', 9, (SELECT Id FROM Categories WHERE Name = 'Electronic devices')),
('PR0011', 'Iphone 17 Pro Max - Apple', 1900, 'Apple', 6, (SELECT Id FROM Categories WHERE Name = 'Electronic devices')),
('PR0012', 'Coffee Maker', 60, 'Panasonic', 11, (SELECT Id FROM Categories WHERE Name = 'Home appliances')),
('PR0013', 'Smart TV', 60, 'Panasonic', 3, (SELECT Id FROM Categories WHERE Name = 'Electronic devices')),
('PR0014', 'Fridge', 2000, 'Whirlpool', 4, (SELECT Id FROM Categories WHERE Name = 'Home appliances')),
('PR0015', 'Laptop MSI, 16RAM', 1200, 'MSI', 2, (SELECT Id FROM Categories WHERE Name = 'Electronic devices')),
('PR0016', 'Car Seat Toyota Tercel', 90, 'Toyota', 3, (SELECT Id FROM Categories WHERE Name = 'Vehicle parts and accessories'));

-- Select all the products
SELECT * FROM Products ORDER BY Name;

-- Select products where Price > 50000
SELECT p.Name AS ProductName, p.Code, p.Price, p.Brand, p.StockAvailable, c.Name AS CategoryName, p.EntryDate
FROM Products p 
LEFT JOIN Categories c ON p.CategoryId = c.Id
WHERE p.Price > 50000
ORDER BY p.Name;

-- Select products where ProductName = 'apple' by using LIKE
SELECT p.Name AS ProductName, p.Code, p.Price, p.Brand, p.StockAvailable, c.Name AS CategoryName, p.EntryDate
FROM Products p 
LEFT JOIN Categories c ON p.CategoryId = c.Id
WHERE p.Name LIKE '%apple%'
ORDER BY p.Name;

-- Get the 5 more expensive products ORDER BY Price DESC LIMIT 5
SELECT p.Name AS ProductName, p.Code, p.Price, p.Brand, p.StockAvailable, c.Name AS CategoryName, p.EntryDate
FROM Products p 
LEFT JOIN Categories c ON p.CategoryId = c.Id
ORDER BY p.Price DESC LIMIT 5;