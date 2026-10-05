import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2] # /car_rentals_api
DATA_DIR = BASE_DIR / "db" / "db_backups"

def save_data_to_csv(records, file_name, field_names, data_dir=DATA_DIR):
    file_path = Path(data_dir) / file_name
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = file_path.exists() and file_path.stat().st_size > 0

    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        if not file_exists:
            writer.writeheader()
        for record in records:
            writer.writerow(record.to_dict())
            