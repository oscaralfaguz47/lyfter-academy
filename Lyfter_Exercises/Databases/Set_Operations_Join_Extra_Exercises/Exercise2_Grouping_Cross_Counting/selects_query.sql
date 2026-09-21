-- GROUPING AND CROSS COUNTING EXERCISES

-- * Get the total number of times that a Customer has rented a book
-- * Order from highest to lowest and limit the result to the 3 more active customers. 
SELECT 
customers.Name AS CustomerName,
COUNT(rents.Id) AS RentedNumTimes
 FROM Customers customers
INNER JOIN Rents rents ON customers.Id = rents.CustomerId
GROUP BY customers.Id, customers.Name
ORDER BY COUNT(rents.Id) DESC
LIMIT 3;
