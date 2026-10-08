from app.http.errors import ServiceUnavailableError
from app.repositories.exceptions import DatabaseUnavailableError

class SystemHealthService:
    def __init__(self, repository):
        self._repository = repository

    def get_health_tables(self):
        try:
            return self._check_tables()
        except DatabaseUnavailableError as error:
            raise ServiceUnavailableError("The database is not available.") from error

    def _check_tables(self):
        missing_tables = self._repository.get_missing_tables()
        errors = {table: "The table does not exist." for table in missing_tables}
        row_counts = {}

        for table in self._repository.REQUIRED_TABLES:
            if table in missing_tables:
                continue
            num_rows = self._repository.get_num_rows_in_table(table)
            if num_rows == 0:
                errors[table] = "The table has no records."
            else:
                row_counts[table] = num_rows
        if errors: 
            raise ServiceUnavailableError("Some tables are not ready.", errors)
        return row_counts