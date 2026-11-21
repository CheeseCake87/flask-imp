from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError


def hash_password_assert(password: str, hashed_password: str) -> bool:
    """
    Checks a plain password against an Argon2id hash created by hash_password.

    The salt and parameters are read from the hash itself.

    Invalid or malformed hashes return False rather than raising.

    :param password: str - plain password
    :param hashed_password: str - the stored Argon2id hash
    :return bool: True if the password matches, False if not
    """
    try:
        return PasswordHasher().verify(hashed_password, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False
