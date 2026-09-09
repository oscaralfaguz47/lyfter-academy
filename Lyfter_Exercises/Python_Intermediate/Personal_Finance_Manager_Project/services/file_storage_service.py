import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_data_to_csv(record, file_name, field_names, data_dir=DATA_DIR):
    file_path = Path(data_dir) / file_name
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = file_path.exists() and file_path.stat().st_size > 0

    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        if not file_exists:
            writer.writeheader()
        writer.writerow(record.to_dict())


def get_data_from_csv(file_name, model_class, data_dir=DATA_DIR):
    file_path = Path(data_dir) / file_name

    if not file_path.exists():
        return []

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [model_class.from_dict(row) for row in reader]