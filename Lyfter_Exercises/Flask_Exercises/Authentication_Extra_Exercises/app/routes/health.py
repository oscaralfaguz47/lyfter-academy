from http import HTTPStatus
import logging

from flask import Blueprint
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_session

logger = logging.getLogger(__name__)

health_bp = Blueprint("health", __name__)

@health_bp.get("/api/v1/health")
def health():
    try:
        get_session().execute(select(1))
    except SQLAlchemyError:
        logger.exception("Database health check failed")
        return {"status": "error", "database": "unreachable"}, HTTPStatus.SERVICE_UNAVAILABLE
    return {"status": "ok", "database": "ok"}, HTTPStatus.OK