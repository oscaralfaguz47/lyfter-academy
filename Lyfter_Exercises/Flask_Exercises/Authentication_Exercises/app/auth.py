from collections.abc import Callable
from datetime import timedelta
from functools import wraps

from flask import current_app, g, request

from app.errors.exceptions import UnauthorizedError
from app.security.tokens import TokenService, TokenType


def get_token_service() -> TokenService:
    config = current_app.config
    return TokenService(
        secret=config["JWT_SECRET_KEY"],
        access_lifetime=timedelta(minutes=config["JWT_ACCESS_TOKEN_MINUTES"]),
        refresh_lifetime=timedelta(days=config["JWT_REFRESH_TOKEN_DAYS"]),
    )

def login_required[**P, R](view: Callable[P, R]) -> Callable[P, R]:

    @wraps(view) 
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        g.current_user_id = get_token_service().verify(_bearer_token(), TokenType.ACCESS)
        return view(*args, **kwargs)

    return wrapper

def current_user_id() -> int:
    return g.current_user_id

def _bearer_token() -> str:
    header = request.headers.get("Authorization", "")
    scheme, _, token = header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise UnauthorizedError("Missing or malformed Authorization header. Use: Bearer <token>")
    return token.strip()

    