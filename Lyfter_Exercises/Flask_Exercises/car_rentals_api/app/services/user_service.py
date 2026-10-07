import logging
logger = logging.getLogger(__name__)
from app.db import transaction

from app.http.errors import ValidationError, ConflictError, NotFoundError
from app.models.user import User
from app.models.exceptions import ModelValidationError
from app.repositories.exceptions import DuplicateRecordError
from app.utils.validators import clean_bool

class UserService:
    def __init__(self, repository):
        self._repository = repository

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
        
        with transaction():
            try:
                user_created = self._repository.create(user_to_create)
            except DuplicateRecordError as error:
                raise ConflictError("User name or email already in use.") from error
            logger.info("User created")
            return user_created

    def update_user_status(self, user_id, json_data):
        errors ={}
        status = clean_bool(json_data.get("status"), "status", errors)

        if errors:
            raise ValidationError("User data is invalid.", errors)
        with transaction():
            user_updated = self._repository.update_status(user_id, status)
            if user_updated is None:
                raise NotFoundError(f"User {user_id} does not exist.")
            logger.info("User '%s' status changed to %s.", user_id, status)
        return user_updated

    def flag_user_as_non_paying(self, user_id):
        with transaction():
            if self._repository.flag_user_as_non_paying(user_id) is None:
                raise NotFoundError(f"User {user_id} does not exist.")
        return self._repository.find_by_id(user_id)