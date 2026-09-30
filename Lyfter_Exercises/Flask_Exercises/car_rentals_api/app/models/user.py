from datetime import datetime

from app.models.exceptions import ModelValidationError
from app.utils.dates import parse_iso_date

class User:
    def __init__(self, full_name, username, email, password, birthdate, status=True, *, user_id=None, creation_date=None):
        errors = []
        if not isinstance(full_name, str) or not full_name.strip():
            errors["full_name"] = "The full name is required."
        if not isinstance(username, str) or not username.strip():
            errors["username"] = "The username is required."
        if len(username) > 30:
            errors["username"] = "The username must be max 30 characters."
        if not isinstance(email, str) or not email.strip():
            errors["email"] = "The email es required."
        if not isinstance(password, str) or not password.strip():
            errors["password"] = "The password is required."
        if parse_iso_date(birthdate) is None:
            errors["birthdate"] = "The birthdate must be a valid date in YYYY-MM-DD format."
        if not isinstance(status, bool):
            errors["status"] = "The status must be true or false only."
        self.full_name = full_name
        self.username = username
        self.email = email
        self.password = password
        self.birthdate = birthdate
        self.status = status
        self.id = user_id
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if errors:
            raise ModelValidationError(errors)

    @classmethod
    def from_row(cls, row):
        return cls(
            row["full_name"], row["username"], row["email"], row["password"],
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