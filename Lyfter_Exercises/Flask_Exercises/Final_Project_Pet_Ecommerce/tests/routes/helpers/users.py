""" Builders and constants for user and auth route tests. """

EMAIL = "oscar.alfaro@example.com"
PASSWORD = "correct-pass-4557Abc$"

OTHER_EMAIL = "emilio@example.com"
ADMIN_EMAIL = "user-admin@example.com"

PUBLIC_USER_FIELDS = {"id", "name", "phone_number", "email", "created_at", "updated_at", "role"}

def registration_body(**overrides: object) -> dict[str, object]:
    return {
        "name": "Oscar Alfaro Client",
        "email": EMAIL,
        "phone_number": "+506 85318674",
        "password": PASSWORD,
    } | overrides

def login_body(**overrides: object) -> dict[str, object]:
    return {"email": EMAIL, "password": PASSWORD} | overrides

def bearer(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}