-- 1. Get all existing products
SELECT * FROM Products ORDER BY Name;

-- 2. Get all products with price greater than 50000
SELECT * FROM Products WHERE Price > 50000 ORDER BY NAME;

-- 3. Get all the purchases of the same product by Id
SELECT p.Name, pi.Id, pi.ProductId, pi.InvoiceId, pi.Quantity, pi.UnitPrice, pi.TotalAmount FROM ProductInvoice pi
INNER JOIN Products p ON pi.ProductId = p.Id 
WHERE pi.ProductId = (SELECT Id FROM Products WHERE Code = 'PR0001')
ORDER BY p.Name;


-- 4. Get all the purchases group by product, by showing the total amount between all the purchases.
SELECT pi.ProductId, p.Name, SUM(pi.TotalAmount) as TotalPurchased 
FROM ProductInvoice pi
INNER JOIN Products p ON pi.ProductId = p.Id
GROUP BY ProductId
ORDER BY p.Name;

-- 5. Get all issued invoices by the same buyer
SELECT * FROM Invoices WHERE UserId = (SELECT Id FROM Users WHERE Email = 'oscar.alfaguz47@gmail.com');

-- 6. Get all the invoices order by total amount in descending order
SELECT * FROM Invoices ORDER BY TotalAmount DESC;

-- 7. Get only one invoice by Invoice number
SELECT * FROM Invoices WHERE InvoiceNumber = 'INV00002';