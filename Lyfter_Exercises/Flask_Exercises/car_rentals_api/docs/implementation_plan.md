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
|-- docs/implementation_plan.md
|
|-- app/
|   |-- __init__.py
|   |-- config.py
|   |-- db.py
|   |-- errors.py
|   |-- api_response.py
|   |-- models/
|   |   |-- brand.py
|   |   |-- vehicle_model.py
|   |   |-- user.py
|   |   |-- vehicle.py
|   |   |-- rental.py
|   |-- repositories/
|   |   |-- brand_repository.py 
|   |   |-- user_repository.py
|   |   |-- vehicle_model_repository.py
|   |   |-- vehicle_repository.py
|   |   |-- rental_repository.py
|   |-- services/
|   |   |-- brand_service.py
|   |   |-- user_service.py
|   |   |-- vehicle_model_service.py
|   |   |-- vehicle_service.py
|   |   |-- rental_service.py
|   |-- routes/
|   |   |-- brands.py
|   |   |-- users.py
|   |   |-- vehicle_models.py
|   |   |-- vehicles.py
|   |   |-- rentals.py




- Tables to create (migration 001_create_tables.sql) 

users(id, full_name, username, email, password, birthdate, status, creation_date) 

brands(id, name)
vehicle_models(id, name, brand_id)
vehicles(id, model_id, year, status)
rentals(id, user_id, vehicle_id, rental_date, status) 

```
