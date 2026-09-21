### Set operation: All - Odd

All = {1,2,3,4,5,6,7,8,9,10}
Odd = {1,3,5,7,9}

Difference: elements in All that are not in Odd.
Result: {2,4,6,8,10}

### Representation in SQL with JOINs

Each set is a table:

CREATE TABLE AllNumbers(Value INTEGER PRIMARY KEY);
CREATE TABLE OddNumbers(Value INTEGER PRIMARY KEY);

INSERT INTO AllNumbers VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10);
INSERT INTO OddNumbers VALUES (1),(3),(5),(7),(9);

Query:

SELECT a.Value
FROM AllNumbers a
LEFT JOIN OddNumbers o ON o.Value = a.Value
WHERE o.Value IS NULL;

Result: 2, 4, 6, 8, 10

### Which JOIN I'll use and why?

**LEFT JOIN**, filtering with "IS NULL".

1. "LEFT JOIN" keeps all rows from AllNumbers (the left set).
2. If a number is also in OddNumbers, "o.Value" has a value.
3. If it is not in OddNumbers, "o.Value" is NULL.
4. "WHERE o.Value IS NULL" keeps only the numbers that are not in Odd.

An INNER JOIN would not work, because it returns only the matches (All ∩ Odd = {1,3,5,7,9}).

### Alternative without JOIN

SELECT Value FROM AllNumbers
EXCEPT
SELECT Value FROM OddNumbers;