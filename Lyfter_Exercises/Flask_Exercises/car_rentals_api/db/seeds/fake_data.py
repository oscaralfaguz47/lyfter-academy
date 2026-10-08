from datetime import time
import random

from faker import Faker
from psycopg2.extras import RealDictCursor, execute_values

NUM_USERS = 200
NUM_VEHICLES = 100
NUM_RENTALS = 150

fake = Faker() # en_US by default

# ---- BUILD THE FAKE DATA TO INSERT ----

def build_fake_users(count):
    return[
        (
            fake.name(),
            f"{fake.unique.user_name().lower()}{random.randint(100, 999999)}",
            f"{fake.unique.email().lower()}{random.randint(100, 999999)}",
            fake.password(),
            fake.date_of_birth(minimum_age=18, maximum_age=75)
        )
        for _ in range(count)
    ]

def build_fake_vehicles(count, model_ids):
    return [
        (
            random.choice(model_ids),
            random.randint(2010, 2027),
            "Available"
        )
        for _ in range(count)
    ]
def build_fake_rentals(count, user_ids, vehicle_ids):
    return [
        (
            random.choice(user_ids),
            random.choice(vehicle_ids),
            "Completed"
        )
        for _ in range(count)
    ]
    
# ---- GET EXISTING MODELS ----
def get_vehicle_models_ids(cursor):
    cursor.execute(f"SELECT id FROM vehicle_models")
    model_ids = [row["id"] for row in cursor.fetchall()]
    if not model_ids:
        raise RuntimeError("Seed vehicle_models before creating vehicles.")
    return model_ids

# ---- INSERTS ----

# Inserts the users and returns the ids
def insert_users(cursor, users):
    query = f"""
        INSERT INTO users (full_name, username, email, password, birthdate)
        VALUES %s
        RETURNING id
    """
    return [row["id"] for row in execute_values(cursor, query, users, fetch=True)]

# Inserts the vehicles and returns the ids
def insert_vehicles(cursor, vehicles):
    query = f"""
        INSERT INTO vehicles (model_id, year, status)
        VALUES %s
        RETURNING id
    """
    rows = execute_values(cursor, query, vehicles, fetch=True)
    return [row["id"] for row in rows]

# Inserts the rentals and returns the ids
def insert_rentals(cursor, rentals):
    query = f"""
        INSERT INTO rentals (user_id, vehicle_id, status)
        VALUES %s
        RETURNING id
    """
    rows = execute_values(cursor, query, rentals, fetch=True)
    return [row["id"] for row in rows]

# ---- ENTRY POINT ----
def seed_fake_data(connection):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            user_ids = insert_users(cursor, build_fake_users(NUM_USERS))
            model_ids = get_vehicle_models_ids(cursor)
            vehicle_ids = insert_vehicles(cursor, build_fake_vehicles(NUM_VEHICLES, model_ids))
            rentals = insert_rentals(cursor, build_fake_rentals(NUM_RENTALS, user_ids, vehicle_ids))

    return {"users": len(user_ids), "vehicles": len(vehicle_ids), "rentals": len(rentals)}