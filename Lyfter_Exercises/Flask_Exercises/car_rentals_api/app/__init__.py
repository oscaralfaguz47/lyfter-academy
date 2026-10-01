import logging

from flask import Flask, request

from app.errors import register_error_handlers
from app.api_response import ApiResponse
from app import db
from app.config import DevelopmentConfig
from app.services.user_service import UserService
from app.services.vehicle_service import VehicleService
from app.repositories.user_repository import UserRepository
from app.repositories.vehicle_repository import VehicleRepository

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

    # ----------------- USERS -----------------
    # List of user filtering by username: users?username=oscar
    @app.route("/users", methods=["GET"])
    def list_users_handler():
        username = request.args.get("username")
        user_service = UserService(UserRepository())
        users_list = user_service.list_users(username)
        return ApiResponse.success("Users retrieved successfully", [user.to_dict() for user in users_list])

    @app.route("/users", methods=["POST"])
    def create_user_handler():
        user_service = UserService(UserRepository())
        user_created = user_service.create_user(request.json)
        return ApiResponse.success("User created successfully", user_created.to_dict())

    @app.route("/users/<int:user_id>/status", methods=["PATCH"])
    def change_user_status_handler(user_id):
        user_service = UserService(UserRepository())
        user = user_service.update_user_status(user_id, request.json)
        return ApiResponse.success("User status updated successfully", user.to_dict())


    # ----------------- VEHICLES -----------------
    @app.route("/vehicles", methods=["GET"])
    def list_vehicles_handler():
        model_id = request.args.get("model_id")
        vehicle_service = VehicleService(VehicleRepository())
        vehicles_list = vehicle_service.list_vehicles(model_id)
        return ApiResponse.success(
                "Vehicles retrieved successfully", 
                [vehicle.to_dict() for vehicle in vehicles_list]
            )


    return app