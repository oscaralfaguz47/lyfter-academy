import argparse
import random

from faker import Faker
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_config
from app.database import create_db_engine
from app.models import Address, Brand, User, Vehicle, VehicleModel
from app.models.enums import VehicleStatus

# Fixed catalog: Faker has no car brands, and real names make the data readable
CATALOG = {
    "Toyota": ["Corolla", "Hilux", "RAV4"],
    "Honda": ["Civic", "CR-V"],
    "Nissan": ["Sentra", "Frontier"],
    "Hyundai": ["Tucson", "Elantra"],
}
MAX_ADDRESSES_PER_USER = 3
MAX_VEHICLES_PER_USER = 2
UNASSIGNED_VEHICLES = 5

fake = Faker()

def get_or_create_models(session: Session) -> list[VehicleModel]:
    """ Make sure every brand and model of CATALOG exists, reusing the ones already in the DB """
    models: list[VehicleModel] = []
    for brand_name, model_names in CATALOG.items():
        brand = session.scalar(select(Brand).where(Brand.name == brand_name))
        if brand is None:
            brand = Brand(name=brand_name)
            session.add(brand)

        existing = {model.name: model for model in brand.vehicle_models}
        for model_name in model_names:
            model = existing.get(model_name)
            if model is None:
                model = VehicleModel(name=model_name)
                brand.vehicle_models.append(model) 
            models.append(model)
    return models


def fake_address() -> Address:
    return Address(
        line1=fake.street_address(),
        line2=fake.secondary_address() if random.random() < 0.3 else None,
        city=fake.city(),
        state=fake.state(),
        zip_code=fake.postcode(),
    )


def fake_vehicle(models: list[VehicleModel]) -> Vehicle:
    return Vehicle(
        year=random.randint(2000, 2025),
        status=random.choice(list(VehicleStatus)),
        vehicle_model=random.choice(models),
    )


def fake_user(models: list[VehicleModel]) -> User:
    user = User(name=fake.name(), email=fake.unique.email())
    # Appending to the relationships fills user_id on flush, no manual FK handling
    user.addresses.extend(fake_address() for _ in range(random.randint(1, MAX_ADDRESSES_PER_USER)))
    user.vehicles.extend(fake_vehicle(models) for _ in range(random.randint(0, MAX_VEHICLES_PER_USER)))
    return user


def seed(session: Session, user_count: int) -> None:
    models = get_or_create_models(session)
    users = [fake_user(models) for _ in range(user_count)]
    unassigned = [fake_vehicle(models) for _ in range(UNASSIGNED_VEHICLES)]
    session.add_all(users + unassigned)

    print(f"Users: {len(users)}")
    print(f"Addresses: {sum(len(user.addresses) for user in users)}")
    print(f"Vehicles with owner: {sum(len(user.vehicles) for user in users)}")
    print(f"Vehicles without owner: {len(unassigned)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Insert fake users, addresses and vehicles.")
    parser.add_argument("--users", type=int, default=20, help="How many users to create, default 20.")
    args = parser.parse_args()

    config = get_config()
    engine = create_db_engine(config.DATABASE_URL, config.DB_SCHEMA)
    try:
        # session.begin() commits when the block ends, or rolls back everything if something fails
        with Session(engine) as session, session.begin():
            seed(session, args.users)
        print("Seed committed.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()