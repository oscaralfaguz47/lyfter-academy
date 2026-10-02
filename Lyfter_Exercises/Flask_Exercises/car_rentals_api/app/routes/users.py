from flask import Blueprint, request

from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.http.api_response import ApiResponse

users_bp = Blueprint("users", __name__, url_prefix="/users")

def _service():
    return UserService(UserRepository())

# List of user filtering by username: users?username=oscar
@users_bp.get("")
def list_users_handler():
    username = request.args.get("username")
    users_list = _service().list_users(username)
    return ApiResponse.success("Users retrieved successfully", [user.to_dict() for user in users_list])

@users_bp.post("")
def create_user_handler():
    user_created = _service().create_user(request.json)
    return ApiResponse.success("User created successfully", user_created.to_dict())

@users_bp.patch("/<int:user_id>/status")
def change_user_status_handler(user_id):
    user = _service().update_user_status(user_id, request.json)
    return ApiResponse.success("User status updated successfully", user.to_dict())