from collections.abc import Sequence

from sqlalchemy import select, func, Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload, joinedload

from app.errors.exceptions import ConflictError
from app.models import User, Vehicle, VehicleModel

from app.schemas.user import UserListParams

USER_REFERENCING_CONSTRAINTS = {"fk_addresses_user_id_users", "fk_vehicles_user_id_users"}
SORT_COLUMNS = {"id": User.id, "name": User.name}

class UserRepository:
    # The session is injected and the repository never calls get_session()
    def __init__(self, session: Session) -> None:
        self._session = session

    def list(self, params: UserListParams) -> Sequence[User]:
        query = self._filtered(params).order_by(*_sort_clauses(params.sort)).offset(params.offset).limit(params.per_page)
        return self._session.scalars(query).all()
    
    def get_by_id(self, user_id: int) -> User | None:
        return self._session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self._session.scalar(select(User).where(User.email == email))

    def get_with_vehicles_and_addresses(self, user_id: int) -> User | None:
        return self._session.get(
            User, user_id, options=[
                    selectinload(User.addresses),
                    selectinload(User.vehicles).joinedload(Vehicle.vehicle_model).joinedload(VehicleModel.brand),
                ],
            )


    def count(self, params: UserListParams) -> int:
        query = self._filtered(params).with_only_columns(func.count(User.id))
        return self._session.scalar(query) or 0

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

    def _filtered(self, params: UserListParams) -> Select:
        query = select(User)
        if params.min_vehicles is not None:
            owners = (
                select(Vehicle.user_id)
                .where(Vehicle.user_id.is_not(None))
                .group_by(Vehicle.user_id)
                .having(func.count(Vehicle.id) >= params.min_vehicles)
            )
            query = query.where(User.id.in_(owners))
        return query
    

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

def _sort_clauses(sort: str) -> tuple:
    column = SORT_COLUMNS[sort.lstrip("-")]
    return (column.desc() if sort.startswith("-") else column.asc(), User.id)