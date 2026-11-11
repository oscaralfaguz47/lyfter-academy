import pytest
from pydantic import ValidationError

from app.schemas.user import UserUpdate


def _error_locations(error: ValidationError) -> list[tuple]:
    return [problem["loc"] for problem in error.errors()]


def test_user_update_with_one_field_sets_only_that_field() -> None:
    data = UserUpdate.model_validate({"name": "Oscar"})
    assert data.model_fields_set == {"name"}

def test_user_update_strips_whitespace_and_lowercases_email() -> None:
    data = UserUpdate.model_validate({"name": " Oscar ", "email": "Oscar.Alfaro@Example.COM"})
    assert data.name == "Oscar"
    assert data.email == "oscar.alfaro@example.com"

def test_user_update_with_empty_body_raises() -> None:
    with pytest.raises(ValidationError) as exc_info:
        UserUpdate.model_validate({})
        assert _error_locations(exc_info.value) == [()]

@pytest.mark.parametrize(
    ("body", "field"),
    [
        ({"role": "admin"}, "role"),
        ({"name": None}, "name"),
        ({"phone_number": None}, "phone_number"),
        ({"name": " "}, "name"),
        ({"phone_number": "1" * 21}, "phone_number"),
    ],
    ids=["unknown_role", "null_name", "null_phone", "blank_name", "phone_21_chars"],
)
def test_user_update_with_invalid_field_raises_on_that_field(body: dict, field: str) -> None:
    with pytest.raises(ValidationError) as exc_info:
        UserUpdate.model_validate(body)
    assert _error_locations(exc_info.value) == [(field,)]