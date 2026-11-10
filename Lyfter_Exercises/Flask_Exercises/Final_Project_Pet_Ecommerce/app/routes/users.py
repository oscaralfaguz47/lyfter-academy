from flask import Blueprint, request

from app.database import get_session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRead, UserUpdate, UserListParams
from app.schemas.validation import parse
from app.services.user_service import UserService
from app.routes.responses import serialize, ok, no_content, pagination_meta, serialize_many
from app.auth import permission_required, login_required
from app.security.permissions import Permission
from app.auth import current_actor


users_bp = Blueprint("users", __name__, url_prefix="/api/v1/users")

def _user_service() -> UserService:
    session = get_session()
    return UserService(session, UserRepository(session))


@users_bp.get("")
@permission_required(Permission.USERS_READ)
def list_users():
    params = parse(UserListParams, request.args.to_dict(), "Invalid query parameters.")
    users, total = _user_service().list_users(params)
    meta = pagination_meta(params.page, params.per_page, total)
    return ok(serialize_many(UserRead, users), meta=meta)

@users_bp.get("/<int:user_id>")
@login_required
def get_user(user_id: int):
    user = _user_service().get_user(current_actor(), user_id)
    return ok(serialize(UserRead, user))

@users_bp.patch("/<int:user_id>")
@login_required
def update_user(user_id: int):
    data = parse(UserUpdate, request.get_json())
    user = _user_service().update_user(current_actor(), user_id, data)
    return ok(serialize(UserRead, user))

@users_bp.delete("/<int:user_id>")
@permission_required(Permission.USERS_DELETE)
def delete_user(user_id: int):
    _user_service().delete_user(current_actor(), user_id)
    return no_content()