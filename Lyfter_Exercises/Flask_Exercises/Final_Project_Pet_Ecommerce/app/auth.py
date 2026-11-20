from collections.abc import Callable
from datetime import timedelta
from functools import wraps

from flask import current_app, g, request, Blueprint

from app.errors.exceptions import UnauthorizedError, ForbiddenError
from app.security.tokens import TokenService, TokenType
from app.security.permissions import Actor, Permission
from app.repositories.user_repository import UserRepository
from app.database import get_session


def get_token_service() -> TokenService:
    config = current_app.config
    return TokenService(
        private_key=config["JWT_PRIVATE_KEY"],
        public_key=config["JWT_PUBLIC_KEY"],
        access_lifetime=timedelta(minutes=config["JWT_ACCESS_TOKEN_MINUTES"]),
        refresh_lifetime=timedelta(days=config["JWT_REFRESH_TOKEN_DAYS"]),
    )

def login_required[**P, R](view: Callable[P, R]) -> Callable[P, R]:

    @wraps(view) 
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        g.actor = _authenticate()
        return view(*args, **kwargs)

    return wrapper

def permission_required[**P, R](permission: Permission) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """ 401 if not logged in, 403 if logged in without permission. """
    def decorator(view: Callable[P, R]) -> Callable[P, R]:
        @wraps(view)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            g.actor = _authorize(permission)
            return view(*args, **kwargs)
        return wrapper
    return decorator

def require_permission_for_blueprint(blueprint: Blueprint, permission: Permission) -> None:
    @blueprint.before_request
    def _check_permission() -> None:
        g.actor = _authorize(permission)

def current_actor() -> Actor:
    return g.actor

def current_user_id() -> int:
    return current_actor().id

def _authorize(permission: Permission) -> Actor:
    actor = _authenticate()
    if not actor.can(permission):
        raise ForbiddenError("You don't have permission to perform this action.")
    return actor

def _authenticate() -> Actor:
    claims = get_token_service().verify(_bearer_token(), TokenType.ACCESS)
    user = UserRepository(get_session()).get_by_id(claims.user_id)
    if user is None or user.token_version != claims.version:
        raise UnauthorizedError("Invalid token.")
    return Actor(id=user.id, role=user.role)


def _bearer_token() -> str:
    header = request.headers.get("Authorization", "")
    scheme, _, token = header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise UnauthorizedError("Missing or malformed Authorization header. Use: Bearer <token>")
    return token.strip()

    