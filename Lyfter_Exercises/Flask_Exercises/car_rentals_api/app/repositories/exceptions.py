
class DuplicateRecordError(Exception):
    """ A UNIQUE constraint rejected the write """

class DatabaseUnavailableError(Exception):
    """ DB is not available """

class BackupWriteError(Exception):
    """ A backup file could not be written """