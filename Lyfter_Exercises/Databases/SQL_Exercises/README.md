## IMPORTANT NOTES
**1.** SQLite has dynamic typing, I mean, the type lives in the value and not in the column, so VARCHAR(n) lengths are not enforce, they are kept for documentation         purposes and portability to MySQL/PostgreSQL.
**2.** If we use DATETIME OR TINYNT, they are not going to work, thats why I set the date columns as text and integers as INTEGER.
**3.** In SQLite is not necessary to add the AUTOINCREMENT because INTEGER PRIMARY KEY auto increments, I set them just for documentation purposes.
**4.** We must run P RAGMA foreign_keys = ON; in every connection to ensure the Foreign keys working that are generated automatically only if we reference them.
**5.** DECIMAL(18, 2) has NUMERIC affinity in SQLite, precision is not enforced. For production money handling, storing integer cents is the safer approach.