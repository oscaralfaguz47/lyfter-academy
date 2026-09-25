
from http import HTTPStatus
from http.client import HTTPException
from api_response import ApiResponse


class APIError(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, errors=None):
        super().__init__(message)
        self.message = message
        self.errors = errors or {}

class ValidationError(APIError):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY

class NotFound(APIError):
    status_code = HTTPStatus.NOT_FOUND

def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(error):
        return ApiResponse.error(error.message, error.status_code, error.errors)

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return ApiResponse.error(error.description, error.code)

    @app.errorhandler(Exception)
    def handle_unexpected(error):
        app.logger.exception("Unhandled error")
        return ApiResponse.error("Something went wrong.", HTTPStatus.INTERNAL_SERVER_ERROR)