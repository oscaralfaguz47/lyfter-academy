""" Shapes of the authentication requests and responses. """

from typing import Annotated, TypeAlias

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.schemas.user import NormalizedEmail, UserCreate

Password: TypeAlias = Annotated[str, StringConstraints(strip_whitespace=False), Field(min_length=8, max_length=128)]
LoginPassword: TypeAlias = Annotated[str, StringConstraints(strip_whitespace=False), Field(min_length=1, max_length=128)]

class RegisterRequest(UserCreate):
    """ Body of POST /auth/register, the normal user fields plus a password. """
    password: Password

class LoginRequest(BaseModel):
    """ Body of POST /auth/login, no password rules here, just check it. """
    model_config = ConfigDict(extra="forbid")

    email: NormalizedEmail
    password: LoginPassword

class RefreshRequest(BaseModel):
    """ Body of POST /auth/refresh. """
    model_config = ConfigDict(extra="forbid")

    refresh_token: Annotated[str, Field(min_length=1)]

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
