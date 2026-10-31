import argparse

from sqlalchemy.orm import Session

from app.config import get_config
from app.database import create_db_engine
from app.repositories.user_repository import UserRepository


def print_user_with_vehicles_and_addresses(session: Session, user_id: int) -> None:
    user = UserRepository(session).get_with_vehicles_and_addresses(user_id)
    if user is None:
        print(f"User {user_id} not found.")

    print(f"User: ID:{user.id}, Name:{user.name}, Email: {user.email} ")

    print(f"\nVehicles ({len(user.vehicles)}):")
    for vehicle in user.vehicles:
        model = vehicle.vehicle_model
        print(f"  - #{vehicle.id} {model.brand.name} {model.name} {vehicle.year} [{vehicle.status}]")

    print(f"\nAddresses ({len(user.addresses)}):")
    for address in user.addresses:
        line2 = f", {address.line2}" if address.line2 else ""
        print(f"  - #{address.id} {address.line1}{line2}, {address.city}, {address.state} {address.zip_code}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Print the vehicles and addresses of a user.")
    parser.add_argument("user_id", type=int)
    args = parser.parse_args()

    config = get_config()
    engine = create_db_engine(config.DATABASE_URL, config.DB_SCHEMA)
    try:
        with Session(engine) as session:
            print_user_with_vehicles_and_addresses(session, args.user_id)
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()