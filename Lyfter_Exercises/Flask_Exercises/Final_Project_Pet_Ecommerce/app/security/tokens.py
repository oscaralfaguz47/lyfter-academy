""" Create and verify JWTs. It knows nothing about Flask or HTTP. """

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum

import jwt

from app.errors.exceptions import UnauthorizedError

ALGORITHM = "RS256"



class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"

@dataclass(frozen=True)
class TokenClaims:
    user_id: int
    version: int

@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str
    expires_in: int  # Seconds until the access token expires


class TokenService:
    def __init__(self, private_key: str, public_key: str, access_lifetime: timedelta, refresh_lifetime: timedelta) -> None:        
        self._private_key = private_key
        self._public_key = public_key
        self._lifetimes = {TokenType.ACCESS: access_lifetime, TokenType.REFRESH: refresh_lifetime}

    def create_pair(self, user_id: int, version: int) -> TokenPair:
        return TokenPair(
            access_token=self._encode(user_id, version, TokenType.ACCESS),
            refresh_token=self._encode(user_id, version, TokenType.REFRESH),
            expires_in=int(self._lifetimes[TokenType.ACCESS].total_seconds()),
        )

    def verify(self, token: str, expected_type: TokenType) -> TokenClaims:
        """ Return the claims of a valid token of 'expected_type', or raise UnauthorizedError. """
        try: 
            claims = jwt.decode(
                token,
                self._public_key,
                algorithms=[ALGORITHM],
                options={"require": ["sub", "type", "ver", "iat", "exp"]},
            )
        except jwt.ExpiredSignatureError as error:
            raise UnauthorizedError("Token has expired.") from error
        except jwt.InvalidTokenError as error: 
            raise UnauthorizedError("Invalid token.") from error

        if claims["type"] != expected_type:
            raise UnauthorizedError("Invalid token.")
        return TokenClaims(user_id=int(claims["sub"]), version=int(claims["ver"]))
        

    def _encode(self, user_id: int, version: int, token_type: TokenType) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user_id),
            "type": token_type.value,
            "ver": version,
            "iat": now,
            "exp": now + self._lifetimes[token_type]
        }
        return jwt.encode(payload, self._private_key, algorithm=ALGORITHM)