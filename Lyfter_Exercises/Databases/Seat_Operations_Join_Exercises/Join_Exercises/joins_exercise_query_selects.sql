-- 1. Get all the Books with its Authors 
SELECT 
books.Id AS BookId, 
books.Name AS BookName, 
books.AuthorId,
authors.Name AS AuthorName
FROM Books books 
FULL OUTER JOIN Authors authors ON books.AuthorId = authors.Id;

-- 2. Get all the Books that don't have Author
SELECT 
books.Id AS BookId, 
books.Name AS BookName
FROM Books books 
LEFT JOIN Authors authors ON books.AuthorId = authors.Id
WHERE authors.Id IS NULL;

-- 3. Get all the Authors that don't have Books
SELECT 
authors.Id AS AuthorId,
authors.Name AS AuthorName
FROM Books books 
RIGHT JOIN Authors authors ON books.AuthorId = authors.Id
WHERE books.Id IS NULL;

-- 4. Get all the Books that have been rented at some time
SELECT  
books.Id AS BookId,
books.Name AS BookName
FROM Books books
INNER JOIN Rents rents ON books.Id = rents.BookId;

-- 5. Get all the Books that have never rented before
SELECT  
books.Id AS BookId,
books.Name AS BookName
FROM Books books
LEFT JOIN Rents rents ON books.Id = rents.BookId
WHERE rents.State IS NULL;

-- 6. Get all the Customers that have never rented a Book
SELECT
customers.Id AS CustomerId, 
customers.Name as CustomerName,
customers.Email
FROM Customers customers
LEFT JOIN Rents rents ON customers.Id = rents.CustomerId
WHERE rents.State IS NULL;

-- 7. Get all the Books que have been rented and are in State "Overdue"
SELECT  
books.Id AS BookId,
books.Name AS BookName
FROM Books books
INNER JOIN Rents rents ON books.Id = rents.BookId
WHERE rents.State = 'Overdue';
