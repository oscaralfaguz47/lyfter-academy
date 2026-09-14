-- EXERCISE 1

-- Create categories and adjust products
CREATE TABLE Categories(
    Id INTEGER PRIMARY KEY,
    Name TEXT UNIQUE NOT NULL,
    Description TEXT
);

-- Add CategoryId to Products table
ALTER TABLE Products ADD CategoryId INTEGER NULL REFERENCES Categories(Id);
-- Add Index for performance
CREATE INDEX IX_Products_CategoryId ON Products(CategoryId);

-- Insert Categories
INSERT INTO Categories (Name, Description) VALUES 
('Clothing and footwear', 'Everything regarding clothing ans shoes'),
('Vehicles', 'Everything you need about vehicles, motorcycles, and more.'),
('Vehicle parts and accessories', 'Everything you need for your car, truck or motorcycle'),
('Home appliances', 'Everything you need for your home'),
('Electronic devices', 'Cellphones, TVs, Laptops, etc.');

-- Update products linking the category
UPDATE Products SET CategoryId = (SELECT Id FROM Categories WHERE Name = 'Clothing and footwear')
WHERE Code IN('PR0001', 'PR0002', 'PR0003', 'PR0003');

UPDATE Products SET CategoryId = (SELECT Id FROM Categories WHERE Name = 'Vehicles')
WHERE Code IN('PR0005', 'PR0006');

-- Verify the categories where linked successfully in Products table
SELECT p.Id, p.Name AS ProductName, p.Price, p.CategoryId, c.Name AS CategoryName, p.StockAvailable FROM Products p
INNER JOIN Categories c ON p.CategoryId = c.Id;

