from flask import Blueprint, request, url_for

from app.auth import get_token_service, login_required, current_actor
from app.database import get_session
from app.repositories.user_repository import UserRepository
from app.routes.responses import created, ok, serialize, no_content
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserRead, MeRead
from app.schemas.validation import parse
from app.security.tokens import TokenPair
from app.services.auth_service import AuthService
from app.services.user_service import UserService

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

def _auth_service() -> AuthService:
    session = get_session()
    return AuthService(session, UserRepository(session), get_token_service())

def _tokens_body(tokens: TokenPair) -> dict:
    return TokenResponse(**vars(tokens)).model_dump()


@auth_bp.post("/register")
def register():
    data = parse(RegisterRequest, request.get_json())
    user, tokens = _auth_service().register(data)
    body = {"user": serialize(UserRead, user), **_tokens_body(tokens)}
    return created(body, location=url_for("users.get_user", user_id=user.id))

@auth_bp.post("/login")
def login():
    data = parse(LoginRequest, request.get_json())
    return ok(_tokens_body(_auth_service().login(data)))

@auth_bp.post("/refresh")
def refresh():
    data = parse(RefreshRequest, request.get_json())
    return ok(_tokens_body(_auth_service().refresh(data.refresh_token)))

@auth_bp.get("/me")
@login_required
def me():
    session = get_session()
    actor = current_actor()
    user = UserService(session, UserRepository(session)).get_user(actor, actor.id)
    return ok(serialize(MeRead, user))

@auth_bp.post("/logout")
@login_required
def logout():
    _auth_service().logout(current_actor().id)
    return no_content()