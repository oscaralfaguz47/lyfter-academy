import csv
from pathlib import Path
from app.http.errors import BackupError


BASE_DIR = Path(__file__).resolve().parents[2] # /car_rentals_api
DATA_DIR = BASE_DIR / "db" / "db_backups"

class BackupRepository:
    def save_data_to_csv(self, records, file_name, field_names, data_dir=DATA_DIR):
        file_path = Path(data_dir) / f"{file_name}.csv"
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=field_names)
                writer.writeheader()
                writer.writerows(records)
        except (OSError, csv.Error) as error:
            raise BackupError(f"Could not write backup file '{file_path}'") from error
        return file_path
            


            