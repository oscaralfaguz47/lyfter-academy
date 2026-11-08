import pytest

from app.security.passwords import hash_password, verify_password

PASSWORD = "oscar-password-4557Abc$"

@pytest.fixture(scope="module")
def stored_hash() -> str:
    return hash_password(PASSWORD)

def test_hash_password_never_contains_the_plain_text(stored_hash: str) -> None:
    assert PASSWORD not in stored_hash

def test_hash_password_returns_scrypt_salt_and_key(stored_hash: str) -> None:
    algorithm, salt_hex, key_hex = stored_hash.split("$")

    assert algorithm == "scrypt"
    assert len(bytes.fromhex(salt_hex)) == 16
    assert len(bytes.fromhex(key_hex)) == 32

def test_hash_password_same_password_twice_returns_different_hashes() -> None:
    assert hash_password(PASSWORD) != hash_password(PASSWORD)

def test_verify_password_correct_password_returns_true(stored_hash : str) -> None:
    assert verify_password(PASSWORD, stored_hash) is True

@pytest.mark.parametrize(
    "attempt",
    [
        "oscar-wrong-password",
        PASSWORD.upper(),
        f"{PASSWORD} ",
        PASSWORD[:-1],
        "",
    ],
    ids=["different", "uppercase", "trailing_space", "missing_last_char", "empty"],
)
def test_verify_password_with_wrong_password_returns_false(stored_hash: str, attempt: str) -> None:
    assert verify_password(attempt, stored_hash) is False

def test_verify_password_with_unicode_password_returns_true() -> None:
    password = "May-strong-password47667"

    assert verify_password(password, hash_password(password)) is True

