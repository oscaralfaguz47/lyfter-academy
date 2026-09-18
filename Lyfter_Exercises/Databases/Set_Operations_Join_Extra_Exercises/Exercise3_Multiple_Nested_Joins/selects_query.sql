SELECT
customers.Name AS CustomerName,
books.Name AS BookName,
authors.Name AS AuthorName,
rents.State AS RentState
FROM Rents rents
INNER JOIN Customers customers ON rents.CustomerId = customers.Id
INNER JOIN Books books ON rents.BookId = books.Id
LEFT JOIN Authors authors ON books.AuthorId = authors.Id
ORDER BY customers.Name, books.Name, rents.Id
LIMIT 10;
