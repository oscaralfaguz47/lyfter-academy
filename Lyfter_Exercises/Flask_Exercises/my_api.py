from http import HTTPStatus
import uuid
from flask import Flask, request
from api_response import ApiResponse
from task_service import create_task, update_task, get_task, delete_task, get_tasks
from errors import register_error_handlers, ValidationError
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

app = Flask(__name__)
register_error_handlers(app)

@app.route("/tasks", methods=["GET"])
def get_tasks_handler():
    status = request.args.get("status")
    tasks = get_tasks(status)
    return ApiResponse.success(
        "Tasks retrieved successfully",
        [task.to_dict() for task in tasks]
    )

@app.route("/tasks/<id>", methods=["GET"])
def get_task_handler(id):
    try:
        parsed_id = uuid.UUID(id)
    except ValueError as error:
        raise ValidationError("Invalid task id.", {"task_id": "Must be a valid UUID."}) from error
    task = get_task(parsed_id)
    return ApiResponse.success(
        "Task retrieved successfully",
        task.to_dict()
    )

@app.route("/tasks", methods=["POST"])
def create_task_handler():
    new_task = create_task(request.json)
    return ApiResponse.success(
        "Task created successfully", new_task.to_dict(),
        HTTPStatus.CREATED
    )

@app.route("/tasks/<id>", methods=["PATCH"])
def update_task_handler(id):
    try:
        parsed_id = uuid.UUID(id)
        updated_task = update_task(parsed_id, request.json)
    except ValueError as error:
        raise ValidationError("Invalid task id.", {"task_id": "Must be a valid UUID."}) from error
    return ApiResponse.success("Task updated successfully", updated_task.to_dict(), HTTPStatus.OK)


@app.route("/tasks/<id>", methods=["DELETE"])
def delete_task_handler(id):
    try:
        parsed_id = uuid.UUID(id)
    except ValueError as error:
        raise ValidationError("Invalid task id.", {"task_id": "Must be a valid UUID."}) from error
    deleted_task = delete_task(parsed_id)
    return ApiResponse.success(
        "Task deleted successfully",
        deleted_task.to_dict()
    )


if __name__ == "__main__":
    app.run(host="localhost", debug=True)