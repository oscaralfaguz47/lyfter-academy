from flask import Blueprint, request

from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.repositories.rental_repository import RentalRepository
from app.http.api_response import ApiResponse
from app.http.http_utils import QueryParams, get_json_body
from app.models.user import USERNAME_MAX_LENGTH, USERNAME_PATTERN, FULL_NAME_MAX_LENGTH, EMAIL_MAX_LENGTH, EMAIL_PATTERN

users_bp = Blueprint("users", __name__, url_prefix="/users")

def _service():
    return UserService(UserRepository(), RentalRepository())

# List of user filtering by username: users?username=oscar
@users_bp.get("")
def list_users_handler():
    params = QueryParams(allowed={"username", "full_name", "email", "birthdate", "status"})
    username = params.get_str("username", max_length=USERNAME_MAX_LENGTH, pattern=USERNAME_PATTERN)
    full_name = params.get_str("full_name", max_length=FULL_NAME_MAX_LENGTH)
    email = params.get_str("email", max_length=EMAIL_MAX_LENGTH, pattern=EMAIL_PATTERN)
    birthdate = params.get_date("birthdate")
    status = params.get_bool("status")

    params.raise_if_errors()
    users_list = _service().list_users(username, full_name, email, birthdate, status)
    return ApiResponse.success("Users retrieved successfully", [user.to_dict() for user in users_list])

@users_bp.post("")
def create_user_handler():
    user_created = _service().create_user(get_json_body())
    return ApiResponse.success("User created successfully", user_created.to_dict())

@users_bp.patch("/<int:user_id>/status")
def change_user_status_handler(user_id):
    user = _service().update_user_status(user_id, request.json)
    return ApiResponse.success("User status updated successfully", user.to_dict())

@users_bp.get("/<int:user_id>/flag-as-non-paying")
def flag_as_non_paying_handler(user_id):
    response = _service().flag_user_as_non_paying(user_id)
    return ApiResponse.success(response["message"], [ur.to_dict() for ur in response["unpaid_rentals"]])
