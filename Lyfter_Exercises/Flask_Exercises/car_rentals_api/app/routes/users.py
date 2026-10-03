from flask import Blueprint, request

from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.http.api_response import ApiResponse
from app.http.http_utils import QueryParams, get_json_body
from app.models.user import USERNAME_MAX_LENGTH, USERNAME_PATTERN

users_bp = Blueprint("users", __name__, url_prefix="/users")

def _service():
    return UserService(UserRepository())

# List of user filtering by username: users?username=oscar
@users_bp.get("")
def list_users_handler():
    params = QueryParams(allowed={"username"})
    username = params.get_str("username", max_length=USERNAME_MAX_LENGTH, pattern=USERNAME_PATTERN)
    params.raise_if_errors()
    users_list = _service().list_users(username)
    return ApiResponse.success("Users retrieved successfully", [user.to_dict() for user in users_list])

@users_bp.post("")
def create_user_handler():
    user_created = _service().create_user(get_json_body())
    return ApiResponse.success("User created successfully", user_created.to_dict())

@users_bp.patch("/<int:user_id>/status")
def change_user_status_handler(user_id):
    user = _service().update_user_status(user_id, request.json)
    return ApiResponse.success("User status updated successfully", user.to_dict())