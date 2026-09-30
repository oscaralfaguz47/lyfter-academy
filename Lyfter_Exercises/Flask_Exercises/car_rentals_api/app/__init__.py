import logging

from flask import Flask, request

from app.errors import register_error_handlers
from app.api_response import ApiResponse
from app import db
from app.config import DevelopmentConfig
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    register_error_handlers(app)
    app.config.from_object(config_class)
    app.json.sort_keys = False

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )

    db.init_app(app)

    @app.route("/health")
    def health():
        with db.get_connection().cursor() as cursor:
            cursor.execute("SELECT 1") # Just proves the DB answers
        return ApiResponse.success("Status: healthy")

    # List of user filtering by username: users?username=oscar
    @app.route("/users", methods=["GET"])
    def list_users_handler():
        username = request.args.get("username")
        user_services = UserService(UserRepository())
        users_list = user_services.list_users(username)
        return ApiResponse.success("Users retrieved successfully", [user.to_dict() for user in users_list])

    return app