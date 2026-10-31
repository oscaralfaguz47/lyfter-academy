import logging

from sqlalchemy.orm import Session

from app.errors.exceptions import ConflictError, UnauthorizedError
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest
from app.security.passwords import hash_password, verify_password
from app.security.tokens import TokenPair, TokenService, TokenType

logger = logging.getLogger(__name__)

INVALID_CREDENTIALS = "Invalid email or password."


class AuthService:
    def __init__(self, session: Session, users: UserRepository, tokens: TokenService) -> None:
        self._session = session
        self._users = users
        self._tokens = tokens

    def register(self, data: RegisterRequest) -> tuple[User, TokenPair]:
        if self._users.get_by_email(data.email) is not None:
            raise ConflictError(f"A user with email {data.email} already exists.")

        user = User(name=data.name, email=data.email, password_hash=hash_password(data.password))
        self._users.add(user)
        self._session.commit()
        logger.info("Registered user %s", user.id)
        return user, self._tokens.create_pair(user.id)

    def login(self, data: LoginRequest) -> TokenPair:
        user = self._users.get_by_email_with_password(data.email)
        # Sme message whether the email of password is wrong.
        if user is None or not verify_password(data.password, user.password_hash):
            logger.info("Failed, login attempt")
            raise UnauthorizedError(INVALID_CREDENTIALS)
        logger.info("User %s logged in", user.id)
        return self._tokens.create_pair(user.id)

    def refresh(self, refresh_token: str) -> TokenPair:
        user_id = self._tokens.verify(refresh_token, TokenType.REFRESH)
        if self._users.get_by_id(user_id) is None:
            raise UnauthorizedError("Invalid token.") # The user was deleted after the token was issued
        return self._tokens.create_pair(user_id)