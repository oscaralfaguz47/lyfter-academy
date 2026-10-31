""" Create and verify JWTs. It knows nothing about Flask or HTTP. """

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum

import jwt

from app.errors.exceptions import UnauthorizedError

ALGORITHM = "HS256"
MIN_SECRET_BYTES = 32

class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"

@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str
    expires_in: int  # Seconds until the access token expires


class TokenService:
    def __init__(self, secret: str, access_lifetime: timedelta, refresh_lifetime: timedelta) -> None:
        if len(secret.encode("utf-8")) < MIN_SECRET_BYTES:
            raise ValueError(f"JWT_SECRET_KEY must be at least {MIN_SECRET_BYTES} bytes long.")
        
        self._secret = secret
        self._lifetimes = {TokenType.ACCESS: access_lifetime, TokenType.REFRESH: refresh_lifetime}

    def create_pair(self, user_id: int) -> TokenPair:
        return TokenPair(
            access_token=self._encode(user_id, TokenType.ACCESS),
            refresh_token=self._encode(user_id, TokenType.REFRESH),
            expires_in=int(self._lifetimes[TokenType.ACCESS].total_seconds()),
        )

    def verify(self, token: str, expected_type: TokenType) -> int:
        """ Raise the user ID inside a valid token of 'expected_type', or raise UnauthorizedError. """
        try: 
            claims = jwt.decode(
                token,
                self._secret,
                algorithms=[ALGORITHM],
                options={"require": ["sub", "type", "iat", "exp"]},
            )
        except jwt.ExpiredSignatureError as error:
            raise UnauthorizedError("Token has expired.") from error
        except jwt.InvalidTokenError as error: 
            raise UnauthorizedError("Invalid token.") from error

        if claims["type"] != expected_type:
            raise UnauthorizedError("Invalid token.")
        return int(claims["sub"])
        

    def _encode(self, user_id: int, token_type: TokenType) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user_id),
            "type": token_type.value,
            "iat": now,
            "exp": now + self._lifetimes[token_type]
        }
        return jwt.encode(payload, self._secret, algorithm=ALGORITHM)