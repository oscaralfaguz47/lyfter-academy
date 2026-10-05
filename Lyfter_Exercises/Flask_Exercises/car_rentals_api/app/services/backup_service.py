

class BackupService:
    def __init__(self, user_repository, vehicle_repository, rental_repository, backup_repository):
        self._user_repository = user_repository
        self._vehicle_repository = vehicle_repository
        self._rental_repository = rental_repository
        self._backup_repository = backup_repository

    def backup_all_db_data(self):
        users = self._user_repository.get_all_for_backup()
        vehicles = self._vehicle_repository.get_all_for_backup()
        rentals = self._rental_repository.get_all_for_backup()
        
        backed_up_users = self._backup_repository.save_data_to_csv(users, file_name, field_names)


