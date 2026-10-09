""" Domain errors raises by services only. No Flask and no HTTP here """

class DomainError(Exception):
    """ Base class for errors the application raises on purpose """

    def __init__(self, message: str, *, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

class NotFoundError(DomainError):
    """ The requested resource does not exist. """

class ConflictError(DomainError): 
    """ Tehe request conflicts with the current state (duplicate, already taken, etc). """

class ValidationError(DomainError):
    """ The input is well formed but has invalid values. """