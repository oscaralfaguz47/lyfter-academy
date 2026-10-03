import logging
logger = logging.getLogger(__name__)

from app.http.errors import ValidationError, ConflictError, NotFoundError
from app.models.user import User
from app.models.exceptions import ModelValidationError
from app.repositories.exceptions import DuplicateRecordError

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

    def create_user(self, user_data):
        try:
            user_to_create = User.create(
                full_name = user_data.get("full_name"),
                username = user_data.get("username"),
                email = user_data.get("email"), 
                birthdate = user_data.get("birthdate"),
                password = user_data.get("password")
            )
        except ModelValidationError as error:
            raise ValidationError("User data is invalid.", error.errors) from error
        try:
            user_created = self._repository.create(user_to_create)
        except DuplicateRecordError as error:
            raise ConflictError("User name or email already in use.") from error
        logger.info("User created")
        return user_created

    def update_user_status(self, user_id, json_data):
        if not isinstance(json_data, dict):
            raise ValidationError("Body must be a JSON object")
        if "status" not in json_data:
            raise ValidationError("User data is invalid.", {"status": "This field is required."})
        if not isinstance(json_data["status"], bool):
            raise ValidationError("User data is invalid.", {"status": "This field must be a boolean only."})
        user_updated = self._repository.update_status(user_id, json_data["status"])
        if user_updated is None:
            raise NotFoundError(f"User {user_id} does not exist.")
        logger.info("User '%s' status changed to %s.", user_id, json_data["status"])
        return user_updated
    