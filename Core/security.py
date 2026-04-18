import hashlib
import hmac
import os
from base64 import b64decode, b64encode

ITERATIONS = 120_000
SALT_SIZE = 16


def hash_password(password: str) -> str:
    salt = os.urandom(SALT_SIZE)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS,
    )
    return f"{ITERATIONS}${b64encode(salt).decode()}${b64encode(password_hash).decode()}"


def verify_password(password: str, encoded_hash: str) -> bool:
    try:
        iterations_str, salt_b64, hash_b64 = encoded_hash.split("$")
        iterations = int(iterations_str)
        salt = b64decode(salt_b64.encode())
        expected_hash = b64decode(hash_b64.encode())
    except (ValueError, TypeError):
        return False

    current_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )
    return hmac.compare_digest(current_hash, expected_hash)
