from http import HTTPStatus

from flask import jsonify

class ApiResponse:
    @staticmethod
    def success(message, data=None, status=HTTPStatus.OK, headers=None):
        body = {"success": True, "message": message, "data": data}
        return jsonify(body), status, headers or {}

    @staticmethod
    def error(message, status=HTTPStatus.BAD_REQUEST, errors=None):
        body = {"success": False, "message": message}
        if errors:
            body["errors"] = errors
        return jsonify(body), status
