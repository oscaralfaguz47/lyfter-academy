-- Create tables
CREATE TABLE Authors(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL
);

CREATE TABLE Books(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    AuthorId INTEGER NULL REFERENCES Authors(Id)
);

CREATE TABLE Customers(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Email TEXT NOT NULL
);

CREATE TABLE Rents(
    Id INTEGER PRIMARY KEY,
    BookId INTEGER NOT NULL REFERENCES Books(Id),
    CustomerId INTEGER NOT NULL REFERENCES Customers(Id),
    State TEXT NOT NULL
);

-- Create indexes to improve performance
CREATE INDEX IX_Books_AuthorId ON Books(AuthorId);
CREATE INDEX IX_Rents_BookId ON Rents(BookId);
CREATE INDEX IX_Rents_CustomerId ON Rents(CustomerId);

-- Seed all tables

INSERT INTO Authors (Name) VALUES
('Miguel de Cervantes'),
('Dante Alighieri'),
('Takehiko Inoue'),
('Akira Toriyama'),
('Walt Disney');

INSERT INTO Books(Name, AuthorId) VALUES 
('Don Quijote', (SELECT Id FROM Authors WHERE Name = 'Miguel de Cervantes')),
('La Divina Comedia', (SELECT Id FROM Authors WHERE Name = 'Dante Alighieri')),
('Vagabond 1-3', (SELECT Id FROM Authors WHERE Name = 'Takehiko Inoue')),
('Dragon Ball 1', (SELECT Id FROM Authors WHERE Name = 'Akira Toriyama')),
('The Book of the 5 Rings', NULL);

INSERT INTO Customers (Name, Email) VALUES 
('John Doe', 'j.doe@email.com'),
('Jane Doe', 'jane@doe.com'),
('Luke Skywalker', 'darth.son@email.com');

INSERT INTO Rents(BookId, CustomerId, State) VALUES
((SELECT Id FROM Books WHERE Name = 'Don Quijote'), (SELECT Id FROM Customers WHERE Name = 'Jane Doe'), 'Returned'),
((SELECT Id FROM Books WHERE Name = 'La Divina Comedia'), (SELECT Id FROM Customers WHERE Name = 'Jane Doe'), 'Returned'),
((SELECT Id FROM Books WHERE Name = 'Don Quijote'), (SELECT Id FROM Customers WHERE Name = 'John Doe'), 'On time'),
((SELECT Id FROM Books WHERE Name = 'Vagabond 1-3'), (SELECT Id FROM Customers WHERE Name = 'John Doe'), 'On time'),
((SELECT Id FROM Books WHERE Name = 'La Divina Comedia'), (SELECT Id FROM Customers WHERE Name = 'Jane Doe'), 'Overdue');


SELECT * FROM Books;
SELECT * FROM Authors;
SELECT * FROM Customers;
SELECT * FROM Rents;