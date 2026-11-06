
from flask import Blueprint, request
from app.services.login_history_service import LoginHistoryService
from app.database import get_session
from app.repositories.login_history_repository import LoginHistoryRepository
from app.auth import permission_required
from app.security.permissions import Permission
from app.schemas.validation import parse
from app.schemas.login_history import LoginHistoryListParams, LoginHistoryRead
from app.routes.responses import ok, serialize_many, pagination_meta


login_history_bp = Blueprint("login_history", __name__, url_prefix="/api/v1/login-history")

def _login_history_service() -> LoginHistoryService:
    session = get_session()
    return LoginHistoryService(LoginHistoryRepository(session))


@login_history_bp.get("")
@permission_required(Permission.LOGIN_HISTORY_READ)
def list_login_history():
    params = parse(LoginHistoryListParams, request.args.to_dict(), "Invalid query parameters.")
    login_history, total = _login_history_service().list_login_history(params)
    meta = pagination_meta(params.page, params.per_page, total)
    return ok(serialize_many(LoginHistoryRead, login_history), meta=meta)