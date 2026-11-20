
import hashlib
import hmac
import os

SCRYPT_PARAMS = {"n": 2**15, "r": 8, "p": 3, "maxmem": 64 * 1024 * 1024, "dklen": 32}

def _derived_key(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(password.encode(), salt=salt, **SCRYPT_PARAMS)

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    return f"scrypt${salt.hex()}${_derived_key(password, salt).hex()}"

def verify_password(password: str, password_hash: str) -> bool:
    _, salt_hex, key_hex = password_hash.split("$")
    return hmac.compare_digest(_derived_key(password, bytes.fromhex(salt_hex)), bytes.fromhex(key_hex))