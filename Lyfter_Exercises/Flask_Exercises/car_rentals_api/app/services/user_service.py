import logging
logger = logging.getLogger(__name__)

from app.http.errors import ValidationError, ConflictError, NotFoundError
from app.models.user import User
from app.models.exceptions import ModelValidationError
from app.repositories.exceptions import DuplicateRecordError
from app.utils.validators import clean_int

class UserService:
    def __init__(self, repository, rental_repository):
        self._repository = repository
        self._rental_repository = rental_repository

    def list_users(self, username=None, full_name=None, email=None, birthdate=None, status=None):
        return self._repository.find_all(username, full_name, email, birthdate, status)

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
        if "status" not in json_data:
            raise ValidationError("User data is invalid.", {"status": "This field is required."})
        if not isinstance(json_data["status"], bool):
            raise ValidationError("User data is invalid.", {"status": "This field must be a boolean only."})
        user_updated = self._repository.update_status(user_id, json_data["status"])
        if user_updated is None:
            raise NotFoundError(f"User {user_id} does not exist.")
        logger.info("User '%s' status changed to %s.", user_id, json_data["status"])
        return user_updated

    def flag_user_as_non_paying(self, user_id):
        errors = {}
        user_id = clean_int(user_id, "user_id", errors)
        if errors:
            raise ValidationError("User data invalid.", errors)
        unpaid_rentals = self._rental_repository.get_active_rentals_by_user_id(user_id)

        message = ""
        if len(unpaid_rentals) > 0:
            message = f"The user has '{len(unpaid_rentals)}' pending rentals to complete."
        else:
            message = "The user is up to date, no pending rentals were found."
        return {
            "message": message,
            "unpaid_rentals": unpaid_rentals
        }