""" Builders shared by route tests. Each test overrides only the field it cares about. """

def registration_body(**overrides: object) -> dict[str, object]:
    return {
        "name": "Oscar Alfaro Client",
        "email": "oscar.alfaro.test@gmail.com",
        "phone_number": "+506 85318674",
        "password": "oscar-password-4557Abc$",
    } | overrides

def bearer(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}