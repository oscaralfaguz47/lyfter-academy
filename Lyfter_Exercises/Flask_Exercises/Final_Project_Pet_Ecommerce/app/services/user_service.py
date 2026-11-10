import logging
from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.errors.exceptions import ConflictError, NotFoundError, ForbiddenError
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdate, UserListParams
from app.security.permissions import Actor, Permission

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, session: Session, repository: UserRepository) -> None:
        self._session = session
        self._repository = repository

    def list_users(self, params: UserListParams) -> tuple[Sequence[User], int]:
        users = self._repository.list(params)
        return users, self._repository.count(params)

    def get_user(self, actor: Actor, user_id: int) -> User:
        self._ensure_can_access(actor, user_id, Permission.USERS_READ)
        return self._get_or_404(user_id)

    def update_user(self, actor: Actor, user_id: int, data: UserUpdate) -> User:
        self._ensure_can_access(actor, user_id, Permission.USERS_UPDATE)
        user = self._get_or_404(user_id)
        changes = data.model_dump(exclude_unset=True) # Returns only the fields the client sent

        # Here if the user sends their own email again, it's not a conflict
        if "email" in changes and changes["email"] != user.email:
            self._ensure_email_is_not_taken(changes["email"])

        # This is the dynamic way of writing "user.name = value"
        for field, value in changes.items():
            setattr(user, field, value)

        self._repository.save(user)
        self._session.commit()
        logger.info("Update user %s (fields: %s)", user.id, ", ".join(changes))
        return user

    def delete_user(self, actor: Actor, user_id: int) -> None: 
        self._ensure_can_access(actor, user_id, Permission.USERS_DELETE)
        user = self._get_or_404(user_id)
        self._repository.delete(user)
        self._session.commit()
        logger.info("Delete user %s", user_id)


    def _ensure_email_is_not_taken(self, email: str) -> None:
        if self._repository.get_by_email(email) is not None:
            raise ConflictError(f"A user with email {email} already exists.")

    def _ensure_can_access(self, actor: Actor, user_id: int, permission: Permission) -> None:
        if not actor.can_access_user(user_id, permission):
            raise NotFoundError(f"User {user_id} not found.")

    def _get_or_404(self, user_id: int) -> User:
        user = self._repository.get_by_id(user_id)
        if user is None: 
            raise NotFoundError(f"User {user_id} not found.")
        return user