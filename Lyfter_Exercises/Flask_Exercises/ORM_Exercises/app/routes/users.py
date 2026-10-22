from http import HTTPStatus

from flask import Blueprint, request, url_for

from app.database import get_session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.schemas.validation import parse
from app.schemas.pagination import PaginationParams
from app.services.user_service import UserService
from app.routes.responses import created, serialize, ok, no_content, pagination_meta, serialize_many


users_bp = Blueprint("users", __name__, url_prefix="/api/v1/users")


def _user_service() -> UserService:
    session = get_session()
    return UserService(session, UserRepository(session))


@users_bp.get("")
def list_users():
    pagination = parse(PaginationParams, request.args.to_dict(), "Invalid query parameters.")
    users, total = _user_service().list_users(pagination)
    meta = pagination_meta(pagination.page, pagination.per_page, total)
    return ok(serialize_many(UserRead, users), meta=meta)

@users_bp.get("/<int:user_id>")
def get_user(user_id: int):
    user = _user_service().get_user(user_id)
    return ok(serialize(UserRead, user))

@users_bp.post("")
def create_user():
    data = parse(UserCreate, request.get_json())
    user = _user_service().create_user(data)
    return created(serialize(UserRead, user), location=url_for("users.get_user", user_id=user.id))

@users_bp.patch("/<int:user_id>")
def update_user(user_id: int):
    data = parse(UserUpdate, request.get_json())
    user = _user_service().update_user(user_id, data)
    return ok(serialize(UserRead, user))

@users_bp.delete("/<int:user_id>")
def delete_user(user_id: int):
    _user_service().delete_user(user_id)
    return no_content()