""" Shapes the user data that enters and leaves the API """

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    """ Body of POST /users """

    # extra="forbid": unknown fields are rejected
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    # EmailStr validates the email format
    email: EmailStr = Field(max_length=120)

    # Pydantic call the normalize_email method automatically through the @field_validator decorator
    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower()

class UserRead(BaseModel):
    """ What the API returns for a user, never includes sensitive fields """

    model_config = ConfigDict(from_attributes=True) # Read from a SQLAlchemy object instead of only from dicts, ex: user.name

    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime