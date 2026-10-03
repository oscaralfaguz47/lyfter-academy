from dataclasses import dataclass
from datetime import date
import re

from app.models.exceptions import ModelValidationError
from app.utils.validators import clean_str, clean_date, clean_bool

USERNAME_PATTERN = re.compile(r"[A-Za-z0-9]+(?:[._-][A-Za-z0-9]+)*", re.ASCII)
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 30

FULL_NAME_MAX_LENGTH = 100

EMAIL_PATTERN = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+", re.ASCII)
EMAIL_MAX_LENGTH = 80

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 20

BIRTHDATE_MIN = date(1900,1,1)

class User:
    def __init__(self, full_name, username, email, birthdate, status=True, *, user_id=None, creation_date=None, password=None):
        self.full_name = full_name
        self.username = username
        self.email = email
        self.password = password
        self.birthdate = birthdate
        self.status = status
        self.id = user_id
        self.creation_date = creation_date

    @classmethod
    def create(cls, *, full_name, username, email, password, birthdate, status=True):
        errors = {}
        full_name = clean_str(
            full_name, 
            "full_name", 
            errors, 
            strip=True,
            max_length=FULL_NAME_MAX_LENGTH
        )
        username = clean_str(
            username, 
            "username", 
            errors, 
            strip=True,
            min_length=USERNAME_MIN_LENGTH, 
            max_length=USERNAME_MAX_LENGTH, 
            pattern=USERNAME_PATTERN
        )
        email = clean_str(
            email,
            "email",
            errors,
            strip=True,
            max_length=EMAIL_MAX_LENGTH,
            pattern=EMAIL_PATTERN
        )
        password = clean_str(
            password,
            "password",
            errors,
            strip=False,
            min_length=PASSWORD_MIN_LENGTH,
            max_length=PASSWORD_MAX_LENGTH
        )
        birthdate = clean_date(
            birthdate,
            "birthdate",
            errors,
            min_date=BIRTHDATE_MIN,
            max_date=date.today()
        )
        status = clean_bool(
            status, 
            "status", 
            errors
        )
        if errors:
                    raise ModelValidationError(errors)
        return cls(
            full_name, 
            username.lower(), 
            email.lower(), 
            birthdate, 
            status, 
            password=password
        )

    @classmethod
    def from_row(cls, row):
        return cls(
            row["full_name"], row["username"], row["email"],
            row["birthdate"], row["status"], 
            user_id=row["id"], creation_date=row["creation_date"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "username": self.username,
            "email": self.email,
            "birthdate": self.birthdate,
            "status": self.status,
            "creation_date": self.creation_date
        }

@dataclass
class UserSummary:
    id:int
    full_name: str

    def to_dict(self):
        return {"id": self.id, "full_name": self.full_name}