from app.errors import ValidationError

def _parse_username_filter(username):
    if username is None:
        return None
    normalized = username.strip().lower()
    if len(normalized) > 30:
        raise ValidationError("Invalid query params.", {"username": "The username must be max 30 characters."})
    return normalized

class UserService:
    def __init__(self, repository):
        self._repository = repository

    def list_users(self, username=None):
        return self._repository.find_all(_parse_username_filter(username))
    