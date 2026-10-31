from collections.abc import Sequence

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, undefer

from app.errors.exceptions import ConflictError
from app.models import User

USER_REFERENCING_CONSTRAINTS = {"fk_addresses_user_id_users", "fk_vehicles_user_id_users"}

class UserRepository:
    # The session is injected and the repository never calls get_session()
    def __init__(self, session: Session) -> None:
        self._session = session

    def list(self, offset: int, limit: int) -> Sequence[User]:
        query = select(User).order_by(User.id).offset(offset).limit(limit)
        return self._session.scalars(query).all()
    
    def get_by_id(self, user_id: int) -> User | None:
        return self._session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self._session.scalar(select(User).where(User.email == email))

    def get_by_email_with_password(self, email: str) -> User | None:
        """ The only query that loads password_hash """
        query = select(User).where(User.email == email).options(undefer(User.password_hash))
        return self._session.scalar(query)

    def count(self) -> int:
        return self._session.scalar(select(func.count()).select_from(User)) or 0

    def add(self, user: User) -> User:
        self._session.add(user)
        self._flush(user)
        return user

    #  Send pending changes of an existing user to the database
    # SQL Alchemy tracks changes on objects it loaded, so no UPDATE method is needed
    def save(self, user: User) -> User:
        self._flush(user)
        return user

    def delete(self, user: User) -> None:
        self._session.delete(user)
        try:
            self._session.flush()
        except IntegrityError as error:
            if _violated_constraint(error) in USER_REFERENCING_CONSTRAINTS:
                raise ConflictError(f"User {user.id} still has addresses or vehicles assigned.") from error
            raise

    def _flush(self, user: User) -> None:
        try:
            # flush() sends the SQL inside the open transaction, it gives us user.id and triggers constraints checks right now
            self._session.flush() 
        except IntegrityError as error:
            # Postgres rejects the INSERT with the UNIQUE constraint, and we read the constraint failed "uq_users_email"
            if _violated_constraint(error) == "uq_users_email":
                raise ConflictError(f"A user with email {user.email} already exists.") from error
            raise # This other raise throws any other integrity error unchanged


def _violated_constraint(error: IntegrityError) -> str | None:
    diagnostics = getattr(error.orig, "diag", None)
    return getattr(diagnostics, "constraint_name", None)