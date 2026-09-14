INSERT INTO Users (FullName, Email) VALUES 
('Oscar Alfaro Guzmán', 'oscar.alfaguz47@gmail.com'),
('Maria Solis Alfaro', 'maria@gmail.com'),
('Clemencia Guzmán', 'clemen45@gmail.com'),
('Javier Alfaro', 'javier4754@gmail.com');

INSERT INTO Products (Code, Name, Price, Brand, StockAvailable) VALUES 
('PR0001', 'Shoes', 100, 'Nike', 10),
('PR0002', 'Shirt', 80, 'Puma', 5),
('PR0003', 'Socks', 10, 'New Balance', 20),
('PR0004', 'Short', 45, 'Adidas', 15),
('PR0005', 'Motorcycle', 5100, 'Honda', 3),
('PR0006', 'Hilux', 60000, 'Toyota', 5);

INSERT INTO Invoices (InvoiceNumber, TotalAmount, UserId, BuyerPhone, CashierCode) VALUES
('INV00001', 80, (SELECT Id FROM Users WHERE Email = 'oscar.alfaguz47@gmail.com'), '85318674', 'C00001');
INSERT INTO Invoices (InvoiceNumber, TotalAmount, UserId, BuyerPhone, CashierCode) VALUES
('INV00002', 100, (SELECT Id FROM Users WHERE Email = 'maria@gmail.com'), '84314675', 'C00002');
INSERT INTO Invoices (InvoiceNumber, TotalAmount, UserId, BuyerPhone, CashierCode) VALUES
('INV00003', 100, (SELECT Id FROM Users WHERE Email = 'maria@gmail.com'), '84314675', 'C00002');

INSERT INTO ProductInvoice (ProductId, InvoiceId, Quantity, UnitPrice, TotalAmount)
SELECT p.Id, i.Id, 1, p.Price, p.Price * 1
FROM Products p, Invoices i
WHERE p.Code = 'PR0002' AND i.InvoiceNumber = 'INV00001'; 

INSERT INTO ProductInvoice (ProductId, InvoiceId, Quantity, UnitPrice, TotalAmount)
SELECT p.Id, i.Id, 1, p.Price, p.Price * 1
FROM Products p, Invoices i
WHERE p.Code = 'PR0001' AND i.InvoiceNumber = 'INV00002'; 

INSERT INTO ProductInvoice (ProductId, InvoiceId, Quantity, UnitPrice, TotalAmount)
SELECT p.Id, i.Id, 1, p.Price, p.Price * 1
FROM Products p, Invoices i
WHERE p.Code = 'PR0001' AND i.InvoiceNumber = 'INV00003'; 


