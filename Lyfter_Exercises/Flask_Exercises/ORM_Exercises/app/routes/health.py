from http import HTTPStatus

from flask import Blueprint, current_app
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_session

health_bp = Blueprint("health", __name__)

@health_bp.get("/health")
def health():
    try:
        get_session().execute(text("SELECT 1"))
    except SQLAlchemyError:
        current_app.logger.exception("Database health check failed")
        return {"status": "error", "database": "unreachable"}, HTTPStatus.SERVICE_UNAVAILABLE
    return {"status": "ok", "database": "ok"}, HTTPStatus.OK