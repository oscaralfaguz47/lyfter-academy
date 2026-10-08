# PROJECT SETUP AND RUN
- **1.** Activate the course venv, the project's dependencies are installed inside a virtual environment, not in the system's Python. Activate it before installing packages or running any command.  
```bash
source lyfter-academy/venv/bin/activate
``` 
- **2.** create a ```.env``` file in car_rentals_api/ with your local credentials using the car_rentals_api/.env.example as an example.   

- **3.** run the commands below to create the schema, apply the migrations and seed the database with preregistered data.
```bash
python3 car_rentals_api/db/setup_db.py
``` 
Or run the command below to seed **users** and **vehicles** with fake data.
```bash
python3 car_rentals_api/db/setup_db.py --fake
``` 
- **4.** run the command below to run the API:
```bash
flask --app "app:create_app()" run --debug
``` 
