from datetime import date

from app.repositories.exceptions import BackupWriteError
from app.http.errors import BackupError

class BackupService:
    def __init__(self, 
            repository,
            user_repository, 
            vehicle_repository, 
            rental_repository,  
            vehicle_model_repository, 
            brand_repository
        ):
        self._repository = repository
        self._user_repository = user_repository
        self._vehicle_repository = vehicle_repository
        self._rental_repository = rental_repository
        self._vehicle_model_repository = vehicle_model_repository
        self._brand_repository = brand_repository

    def backup_all_db_data(self):
        today = date.today().isoformat()
        sources = [
            ("users", self._user_repository),
            ("brands", self._brand_repository),
            ("vehicle_models", self._vehicle_model_repository),
            ("vehicles", self._vehicle_repository),
            ("rentals", self._rental_repository)
        ]

        backed_up_files = []
        try:
            for name, source_repository in sources:
                records = source_repository.get_all_for_backup()
                file_path = self._repository.save_data_to_csv(records, f"{name}_backup_{today}", source_repository.BACKUP_COLUMNS)
                backed_up_files.append(file_path.name)
        except BackupWriteError as error:
            raise BackupError("Could not write the backup files.") from error
        return backed_up_files
        
    


