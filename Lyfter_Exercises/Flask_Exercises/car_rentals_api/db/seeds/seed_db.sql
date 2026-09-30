-- CREATE USERS
INSERT INTO users (full_name, username, email, password, birthdate, status)
SELECT
    first_names[(n - 1) % 10 + 1] || ' ' || last_names[(n - 1) / 5 % 10 + 1],
    lower(first_names[(n - 1) % 10 + 1]) || '.' || lower(last_names[(n - 1) / 5 % 10 + 1]) || n,
    lower(first_names[(n - 1) % 10 + 1]) || '.' || lower(last_names[(n - 1) / 5 % 10 + 1]) || n || '@example.com',
    'changeme' || n,                                      -- placeholder, see note on hashing
    DATE '1970-01-01' + ((n * 397) % 12775),              -- spread between 1970 and 2004
    n % 10 <> 0                                           -- every 10th user is inactive
FROM generate_series(1, 50) AS n,
     (SELECT ARRAY['Oscar', 'Maria', 'Andres', 'Lucia', 'Carlos',
                   'Sofia', 'Diego', 'Valeria', 'Jose', 'Camila'] AS first_names,
             ARRAY['Alfaro', 'Rojas', 'Vargas', 'Jimenez', 'Mora',
                   'Solano', 'Castro', 'Araya', 'Chaves', 'Quesada'] AS last_names) AS names
WHERE NOT EXISTS (SELECT 1 FROM users);


-- CRATE BRANDS
INSERT INTO brands (name) VALUES
    ('Toyota'), ('Honda'), ('Nissan'), ('Hyundai'), ('Kia'),
    ('Mazda'), ('Suzuki'), ('Mitsubishi'), ('Ford'), ('Chevrolet'),
    ('Volkswagen'), ('Subaru'), ('BMW'), ('Mercedes-Benz'), ('Jeep')
ON CONFLICT (name) DO NOTHING;


-- CREATE VEHICLE MODELS
INSERT INTO vehicle_models (name, brand_id)
SELECT data.model_name, b.id
FROM (VALUES
    ('Toyota', 'Corolla'),    ('Toyota', 'RAV4'),        ('Toyota', 'Hilux'),
    ('Honda', 'Civic'),       ('Honda', 'CR-V'),
    ('Nissan', 'Sentra'),     ('Nissan', 'X-Trail'),     ('Nissan', 'Frontier'),
    ('Hyundai', 'Tucson'),    ('Hyundai', 'Accent'),
    ('Kia', 'Sportage'),      ('Kia', 'Rio'),
    ('Mazda', 'Mazda3'),      ('Mazda', 'CX-5'),
    ('Suzuki', 'Swift'),      ('Suzuki', 'Vitara'),
    ('Mitsubishi', 'Montero'),('Mitsubishi', 'L200'),
    ('Ford', 'Ranger'),       ('Chevrolet', 'Tracker'),
    ('Volkswagen', 'Jetta'),  ('Subaru', 'Forester'),
    ('BMW', 'X3'),            ('Mercedes-Benz', 'C200'),
    ('Jeep', 'Wrangler')
) AS data(brand_name, model_name)
JOIN brands AS b ON b.name = data.brand_name   -- the FK lookup: name -> id
ON CONFLICT (name, brand_id) DO NOTHING;


-- CREATE VEHICLES
INSERT INTO vehicles (model_id, year, status)
SELECT vm.id, data.year, data.status
FROM (VALUES
    ('Toyota',  'Corolla',  2022, 'Rented'),
    ('Toyota',  'RAV4',     2023, 'Available'),
    ('Honda',   'Civic',    2021, 'Rented'),
    ('Nissan',  'Sentra',   2020, 'Available'),
    ('Hyundai', 'Tucson',   2024, 'Rented'),
    ('Kia',     'Sportage', 2023, 'Available'),
    ('Mazda',   'CX-5',     2022, 'Maintenance'),
    ('Suzuki',  'Swift',    2021, 'Available'),
    ('Ford',    'Ranger',   2024, 'Rented'),
    ('Jeep',    'Wrangler', 2023, 'Available')
) AS data(brand_name, model_name, year, status)
JOIN brands AS b          ON b.name = data.brand_name
JOIN vehicle_models AS vm ON vm.brand_id = b.id AND vm.name = data.model_name
WHERE NOT EXISTS (SELECT 1 FROM vehicles);


-- CREATE SOME RENTALS
INSERT INTO rentals (user_id, vehicle_id, rental_date, status)
SELECT
    u.id,
    v.id,
    CASE WHEN v.status = 'Rented'
         THEN now() - (v.position || ' days')::INTERVAL          -- recent, still open
         ELSE now() - ((v.position * 10) || ' days')::INTERVAL   -- older, already returned
    END,
    CASE WHEN v.status = 'Rented' THEN 'Active' ELSE 'Completed' END
FROM (SELECT id, status, ROW_NUMBER() OVER (ORDER BY id) AS position
      FROM vehicles) AS v
JOIN (SELECT id, ROW_NUMBER() OVER (ORDER BY username) AS position
      FROM users
      WHERE status = true) AS u
  ON u.position = v.position
WHERE NOT EXISTS (SELECT 1 FROM rentals);