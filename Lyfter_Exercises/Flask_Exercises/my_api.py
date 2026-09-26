from http import HTTPStatus
from flask import Flask, request
from api_response import ApiResponse
from task_service import create_task, update_task, get_task, delete_task, get_tasks
from errors import register_error_handlers
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
    return ApiResponse.success("Tasks retrieved successfully", [task.to_dict() for task in tasks])

@app.route("/tasks/<uuid:task_id>", methods=["GET"])
def get_task_handler(task_id):
    task = get_task(task_id)
    return ApiResponse.success("Task retrieved successfully", task.to_dict())

@app.route("/tasks", methods=["POST"])
def create_task_handler():
    new_task = create_task(request.json)
    return ApiResponse.success("Task created successfully", new_task.to_dict(), HTTPStatus.CREATED)

@app.route("/tasks/<uuid:task_id>", methods=["PATCH"])
def update_task_handler(task_id):
    updated_task = update_task(task_id, request.json)
    return ApiResponse.success("Task updated successfully", updated_task.to_dict())

@app.route("/tasks/<uuid:task_id>", methods=["DELETE"])
def delete_task_handler(task_id):
    deleted_task = delete_task(task_id)
    return ApiResponse.success("Task deleted successfully", deleted_task.to_dict())


if __name__ == "__main__":
    app.run(host="localhost", debug=True)