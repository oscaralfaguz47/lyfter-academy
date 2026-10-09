# Car Rentals project - Implementation plan
### Structure:

```text 
car_rentals_api/
|-- .env
|-- .env.example
|-- db/
|   |-- migrations/
|   |   |-- 001_create_tables.sql
|   |-- seeds/
|   |   |-- seed_db.sql
|   |__ setup_db.py #(Creates the database, apply pending migrations and run the seeds)
|
|-- docs/
|   |-- implementation_plan.md
|   |-- README.md
|
|-- app/
|   |-- __init__.py
|   |-- config.py
|   |-- db.py
|   |-- http/
|   |   |--_init_.py
|   |   |--api_response.py
|   |   |--errors.py
|   |   |--http_utils.py
|   |-- models/
|   |   |-- enums.py
|   |   |-- exceptions.py
|   |   |-- user.py
|   |   |-- vehicle.py
|   |   |-- rental.py
|   |-- repositories/
|   |   |-- exceptions.py 
|   |   |-- user_repository.py
|   |   |-- vehicle_repository.py
|   |   |-- rental_repository.py
|   |-- services/
|   |   |-- user_service.py
|   |   |-- vehicle_service.py
|   |   |-- rental_service.py
|   |-- routes/
|   |   |-- users.py
|   |   |-- vehicles.py
|   |   |-- rentals.py
|   |-- utils/
|   |   |-- validators.py

```
### Tables to create (migration 001_create_tables.sql) 

- users(id, full_name, username, email, password, birthdate, status, creation_date) 

- brands(id, name)

- vehicle_models(id, name, brand_id)

- vehicles(id, model_id, year, status)

- rentals(id, user_id, vehicle_id, rental_date, status) 
