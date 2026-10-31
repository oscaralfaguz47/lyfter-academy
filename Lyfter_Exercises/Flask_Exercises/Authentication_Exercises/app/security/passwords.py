""" TEMPORARY: MD5 to follow the course. MD5 is not safe for passwords,
    we must replace the body of these 2 functions with scrypt/Argon2 
    for best practices
"""

import hashlib
import hmac


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode("utf-8")).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    return hmac.compare_digest(hash_password(password), password_hash)