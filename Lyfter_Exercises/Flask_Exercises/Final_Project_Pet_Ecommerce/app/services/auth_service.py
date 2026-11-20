import logging

from sqlalchemy.orm import Session

from app.errors.exceptions import ConflictError, UnauthorizedError
from app.models import User
from app.models.login_history import LoginHistory
from app.repositories.user_repository import UserRepository
from app.repositories.login_history_repository import LoginHistoryRepository
from app.schemas.auth import LoginRequest, RegisterRequest
from app.security.passwords import hash_password, verify_password
from app.security.tokens import TokenPair, TokenService, TokenType

logger = logging.getLogger(__name__)

INVALID_CREDENTIALS = "Invalid email or password."
DUMMY_PASSWORD_HASH = hash_password("timing-equalizer")


class AuthService:
    def __init__(self, session: Session, users: UserRepository, login_history: LoginHistoryRepository,  tokens: TokenService) -> None:
        self._session = session
        self._users = users
        self._login_history = login_history
        self._tokens = tokens

    def register(self, data: RegisterRequest) -> tuple[User, TokenPair]:
        if self._users.get_by_email(data.email) is not None:
            raise ConflictError(f"A user with email {data.email} already exists.")

        user = User(name=data.name, email=data.email, password_hash=hash_password(data.password), phone_number=data.phone_number)
        self._users.add(user)
        self._session.commit()
        logger.info("Registered user %s", user.id)
        return user, self._tokens.create_pair(user.id, user.token_version)

    def login(self, data: LoginRequest, ip_address: str | None) -> TokenPair:
        user = self._users.get_by_email_with_password(data.email)
        # Sme message whether the email of password is wrong.
        if user is None:
            verify_password(data.password, DUMMY_PASSWORD_HASH)
            self._record_login_attempt(None, ip_address, success=False)
            raise UnauthorizedError(INVALID_CREDENTIALS)
        if not verify_password(data.password, user.password_hash):
            self._record_login_attempt(user.id, ip_address, success=False)
            logger.info("Failed login attempt for user %s", user.id)
            raise UnauthorizedError(INVALID_CREDENTIALS)
        self._record_login_attempt(user.id, ip_address, success=True)
        logger.info("User %s logged in", user.id)
        return self._tokens.create_pair(user.id, user.token_version)

    def refresh(self, refresh_token: str) -> TokenPair:
        claims = self._tokens.verify(refresh_token, TokenType.REFRESH)
        user = self._users.get_by_id(claims.user_id)
        if user is None or user.token_version != claims.version:
            raise UnauthorizedError("Invalid token.") # The user was deleted after the token was issued
        return self._tokens.create_pair(user.id, user.token_version)

    def logout(self, user_id: int) -> None:
        """ Invalidates every token of this user, on every device. """
        user = self._users.get_by_id(user_id)
        user.token_version += 1
        self._session.commit()
        logger.info("User %s logged out", user_id)

    def _record_login_attempt(self, user_id: int | None, ip_address: str | None, *, success: bool) -> None:
        self._login_history.add(
            LoginHistory(user_id=user_id, user_ip=ip_address, success=success)
        )
        self._session.commit()