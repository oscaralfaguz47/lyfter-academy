from datetime import timedelta

import pytest 
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from app.errors.exceptions import UnauthorizedError
from app.security.tokens import TokenClaims, TokenService, TokenType

ACCESS_LIFETIME = timedelta(minutes=15)
REFRESH_LIFETIME = timedelta(days=7)
USER_ID = 7
VERSION = 2

def _generate_key_pair() -> tuple[str, str]:
    """ A fresh RSA key pair as PEM strings, the same format as the files in keys/. """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()
    return private_pem, public_pem

@pytest.fixture(scope="module")
def key_pair() -> tuple[str, str]:
    return _generate_key_pair()

@pytest.fixture
def token_service(key_pair: tuple[str, str]) -> TokenService:
    private_key, public_key = key_pair
    return TokenService(private_key, public_key, ACCESS_LIFETIME, REFRESH_LIFETIME)

def test_verify_access_token_returns_user_id_and_version(token_service: TokenService) -> None:
    pair = token_service.create_pair(USER_ID, VERSION)
    claims = token_service.verify(pair.access_token, TokenType.ACCESS)
    assert claims == TokenClaims(user_id=USER_ID, version=VERSION)

def test_create_pair_returns_access_lifetime_in_seconds(token_service: TokenService) -> None:
    pair = token_service.create_pair(USER_ID, VERSION)
    assert pair.expires_in == 900

@pytest.mark.parametrize(
    ("token_attribute", "expected_type"),
    [
        ("access_token", TokenType.REFRESH),
        ("refresh_token", TokenType.ACCESS),
    ],
    ids=["access_used_as_refresh", "refresh_used_as_access"],
)
def test_verify_token_of_other_type_raises_invalid_token(token_service: TokenService, token_attribute: str, expected_type: TokenType) -> None:
    token = getattr(token_service.create_pair(USER_ID, VERSION), token_attribute)

    with pytest.raises(UnauthorizedError) as exc_info:
        token_service.verify(token, expected_type)
    assert exc_info.value.message == "Invalid token."

def test_verify_expired_token_raises_token_expired(key_pair: tuple[str, str]) -> None:
    private_key, public_key = key_pair
    expired_service = TokenService(private_key, public_key, timedelta(seconds=-1), REFRESH_LIFETIME)
    token = expired_service.create_pair(USER_ID, VERSION).access_token

    with pytest.raises(UnauthorizedError) as exc_info:
        expired_service.verify(token, TokenType.ACCESS)
    assert exc_info.value.message == "Token has expired."

def test_verify_token_signed_with_other_key_raises_invalid_token(token_service: TokenService) -> None:
    other_private_key, other_public_key = _generate_key_pair()
    attacker_service = TokenService(other_private_key, other_public_key, ACCESS_LIFETIME, REFRESH_LIFETIME)
    forget_token = attacker_service.create_pair(USER_ID, VERSION).access_token

    with pytest.raises(UnauthorizedError) as exc_info:
        token_service.verify(forget_token, TokenType.ACCESS)
    assert exc_info.value.message == "Invalid token."

def test_verify_malformed_token_raises_invalid_token(token_service: TokenService) -> None:
    with pytest.raises(UnauthorizedError) as exc_info:
        token_service.verify("non-a-jwt", TokenType.ACCESS)
    assert exc_info.value.message == "Invalid token."

