from flask import Blueprint, request, url_for

from app.database import get_session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRead, UserUpdate, UserListParams, AdminUserCreate, UserRoleUpdate
from app.schemas.validation import parse
from app.services.user_service import UserService
from app.routes.responses import serialize, ok, no_content, pagination_meta, serialize_many, created
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

@users_bp.post("")
@permission_required(Permission.USERS_CREATE)
def create_user():
    data = parse(AdminUserCreate, request.get_json())
    user = _user_service().create_user(current_actor(), data)
    return created(serialize(UserRead, user), location=url_for("users.get_user", user_id=user.id))

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

@users_bp.patch("/<int:user_id>/role")
@permission_required(Permission.USERS_CHANGE_ROLE)
def change_user_role(user_id: int):
    data = parse(UserRoleUpdate, request.get_json())
    user = _user_service().change_role(current_actor(), user_id, data.role)
    return ok(serialize(UserRead, user))