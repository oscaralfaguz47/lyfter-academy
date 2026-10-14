from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.errors.exceptions import ConflictError
from app.models import User


class UserRepository:
    # The session is injected and the repository never calls get_session()
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, user_id: int) -> User | None:
        return self._session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self._session.scalar(select(User).where(User.email == email))

    def add(self, user: User) -> User:
        self._session.add(user)
        try:
            # flush() sends the SQL inside the open transaction, it gives us user.id and triggers constraints checks right now
            self._session.flush() 
        except IntegrityError as error:
            # Postgres rejects the INSERT with the UNIQUE constraint, and we read the constraint failed "uq_users_email"
            if _violated_constraint(error) == "uq_users_email":
                raise ConflictError(f"A user with email {user.email} already exists.") from error
            raise # This other raise throws any other integrity error unchanged
        return user

def _violated_constraint(error: IntegrityError) -> str | None:
    diagnostics = getattr(error.orig, "diag", None)
    return getattr(diagnostics, "constraint_name", None)