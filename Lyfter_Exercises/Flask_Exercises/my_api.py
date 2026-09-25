from http import HTTPStatus
from flask import Flask, request
from api_response import ApiResponse
from task_service import create_task
from errors import register_error_handlers

app = Flask(__name__)
register_error_handlers(app)

@app.route("/tasks", methods=["POST"])
def create_task_handler():
    new_task = create_task(request.json)
    return ApiResponse.success(
        "The task was created successfully", new_task.to_dict(),
        HTTPStatus.CREATED
    )


if __name__ == "__main__":
    app.run(host="localhost", debug=True)