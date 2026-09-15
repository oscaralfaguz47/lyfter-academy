-- EXERCISE 3

-- Set Stock available = 0 where Price <= 0
UPDATE Products SET StockAvailable = 0 WHERE Price <= 0;

-- Increase the Price to 100 units for all products when StockAvailable is < 10
UPDATE Products SET Price = Price + 100 WHERE StockAvailable < 10;

-- Decrease the StockAvailable in 1 for a specific ProductId
UPDATE Products SET StockAvailable = StockAvailable - 1 WHERE Id = 3

-- Verify SELECT * FROM Products ORDER BY Id ASC LIMIT 10
SELECT * FROM Products ORDER BY Id ASC LIMIT 10
