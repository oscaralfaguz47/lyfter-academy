CREATE SCHEMA IF NOT EXISTS transactions_exercises;
SET search_path TO transactions_exercises;

DROP TABLE IF EXISTS bill_lines, bills, products, users;

---- CREATE TABLES ---- 
CREATE TABLE users(
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	user_name VARCHAR(30) NOT NULL,
	email VARCHAR(80) NOT NULL,
	is_active BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE products(
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR(30) NOT NULL,
	price NUMERIC(18,2) NOT NULL CHECK (price > 0),
	stock_available NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (stock_available >=0)
);

CREATE TABLE bills(
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	bill_number INTEGER NOT NULL UNIQUE,
	user_id INTEGER NOT NULL REFERENCES users(id),
	created_at timestamptz NOT NULL DEFAULT now(),
	status VARCHAR(10) NOT NULL DEFAULT 'Sent' CHECK(status IN ('Sent', 'Returned', 'Cancelled'))
);

CREATE TABLE bill_lines(
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	bill_id INTEGER NOT NULL REFERENCES bills(id),
	product_id INTEGER NOT NULL REFERENCES products(id),
	quantity NUMERIC(10,3) NOT NULL CHECK (quantity > 0),
	unit_price NUMERIC(18,2) NOT NULL CHECK (unit_price > 0),
	total_amount NUMERIC(18,2) GENERATED ALWAYS AS (ROUND(quantity * unit_price, 2)) STORED,
	UNIQUE(bill_id, product_id)
);

---- CREATE INDEXES TO IMPROVE PERFORMANCE ----
CREATE UNIQUE INDEX IF NOT EXISTS ux_users_user_name ON users(LOWER(user_name));
CREATE UNIQUE INDEX IF NOT EXISTS ux_users_email ON users(LOWER(email));
CREATE INDEX IF NOT EXISTS ix_bills_user_id ON bills(user_id);
CREATE INDEX IF NOT EXISTS ix_bill_lines_product_id ON bill_lines(product_id);

---- SEED THE TABLES ----

BEGIN;

-- Active Users
INSERT INTO users(user_name, email) VALUES
('oscar',        'oscar@mail.com'),
('ana.rivera',   'ana.rivera@mail.com'),
('luis.mendez',  'luis.mendez@mail.com'),
('marco.gomez',  'marco.gomez@mail.com'),
('carla.ruiz',   'carla.ruiz@mail.com'),
('diana.vargas', 'diana.vargas@mail.com'),
('edwin.mora',   'edwin.mora@mail.com'),
('laura.rojas',  'laura.rojas@mail.com'),
('juan.perez',   'juan.perez@mail.com');

-- Inactive User
INSERT INTO users(user_name, email, is_active) VALUES
('jane.doe', 'jane.doe@mail.com', false);

-- Products
INSERT INTO products(name, price, stock_available) VALUES
('Rice 1kg',            2.50, 100.00),
('Black Beans 1kg',     3.20,  80.00),
('Coffee 500g',         7.90,  50.00),
('Whole Milk 1L',       1.80, 120.00),
('Cheese per kg',      12.50,  25.00),
('Chicken Breast kg',   8.75,  40.00),
('Apples per kg',       4.30,  60.00),
('Olive Oil 750ml',    11.40,  30.00),
('Brown Sugar 2kg',     3.60,  70.00),
('Tomatoes per kg',     2.90,  45.00);

-- Bills (user found by email)
INSERT INTO bills(bill_number, user_id, created_at, status)
SELECT v.bill_number, u.id, v.created_at::timestamptz, v.status
FROM (VALUES
    (1001, 'oscar@mail.com',        '2026-09-01 09:15:00-06', 'Sent'),
    (1002, 'ana.rivera@mail.com',   '2026-09-02 10:30:00-06', 'Sent'),
    (1003, 'luis.mendez@mail.com',  '2026-09-03 11:45:00-06', 'Sent'),
    (1004, 'marco.gomez@mail.com',  '2026-09-04 14:20:00-06', 'Sent'),
    (1005, 'carla.ruiz@mail.com',   '2026-09-05 16:05:00-06', 'Cancelled'),
    (1006, 'diana.vargas@mail.com', '2026-09-06 08:50:00-06', 'Sent'),
    (1007, 'edwin.mora@mail.com',   '2026-09-07 13:10:00-06', 'Sent'),
    (1008, 'laura.rojas@mail.com',  '2026-09-08 17:35:00-06', 'Sent'),
    (1009, 'juan.perez@mail.com',   '2026-09-09 12:00:00-06', 'Sent'),
    (1010, 'oscar@mail.com',        '2026-09-10 18:25:00-06', 'Sent')
) AS v(bill_number, email, created_at, status)
JOIN users u ON LOWER(u.email) = LOWER(v.email);

-- bill_lines (unit_price copied from the product, total_amount is calculated)
INSERT INTO bill_lines(bill_id, product_id, quantity, unit_price)
SELECT b.id, p.id, v.quantity, p.price
FROM (VALUES
    (1001, 'Rice 1kg',           2.00),
    (1001, 'Coffee 500g',        1.00),
    (1001, 'Cheese per kg',      0.70),
    (1002, 'Chicken Breast kg',  1.5),
    (1002, 'Tomatoes per kg',    2.25),
    (1003, 'Whole Milk 1L',      6.00),
    (1003, 'Brown Sugar 2kg',    1.50),
    (1004, 'Apples per kg',      1.20),
    (1004, 'Olive Oil 750ml',    1.00),
    (1005, 'Black Beans 1kg',    3.00),
    (1006, 'Rice 1kg',           1.00),
    (1006, 'Whole Milk 1L',      2.00),
    (1007, 'Coffee 500g',        2.00),
    (1007, 'Cheese per kg',      0.50),
    (1008, 'Tomatoes per kg',    1.00),
    (1009, 'Chicken Breast kg',  2.00),
    (1009, 'Black Beans 1kg',    2.00),
    (1010, 'Olive Oil 750ml',    2.00),
    (1010, 'Apples per kg',      0.80)
) AS v(bill_number, product_name, quantity)
JOIN bills b ON b.bill_number = v.bill_number
JOIN products p ON p.name = v.product_name;

COMMIT;

