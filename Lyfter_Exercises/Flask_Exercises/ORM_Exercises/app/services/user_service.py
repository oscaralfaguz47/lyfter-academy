import logging

from sqlalchemy.orm import Session

from app.errors.exceptions import ConflictError, NotFoundError
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, session: Session, repository: UserRepository) -> None:
        self._session = session
        self._repository = repository

    def get_user(self, user_id: int) -> User:
        user = self._repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User {user_id} not found.")
        return user

    def create_user(self, data: UserCreate) -> User:
        if self._repository.get_by_email(data.email) is not None:
            raise ConflictError(f"A user with email {data.email} already exists.")
        user = self._repository.add(User(name=data.name, email=data.email))
        self._session.commit()
        logger.info("Created user %s", user.id)
        return user