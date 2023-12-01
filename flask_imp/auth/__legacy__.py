import typing as t
from random import choice
from string import ascii_letters

from .authenticate_password import authenticate_password
from .encrypt_password import encrypt_password
from .generate_alphanumeric_validator import generate_alphanumeric_validator
from .generate_csrf_token import generate_csrf_token
from .generate_email_validator import generate_email_validator
from .generate_numeric_validator import generate_numeric_validator
from .generate_password import generate_password
from .generate_private_key import generate_private_key
from .generate_salt import generate_salt
from .is_email_address_valid import is_email_address_valid
from .is_username_valid import is_username_valid


def auth_password(
    cls,
    input_password: str,
    database_password: str,
    database_salt: str,
    encrypt: int = 512,
    pepper_length: int = 1,
) -> bool:
    """Legacy method, use authenticate_password instead"""
    return cls.authenticate_password(
        input_password, database_password, database_salt, encrypt, pepper_length
    )


def hash_password(
    password: str, salt: str, encrypt: int = 512, pepper_length: int = 1
) -> str:
    """Legacy method, use encrypt_password instead"""
    return encrypt_password(password, salt, encrypt, pepper_length)


def sha_password(
    password: str, salt: str, encrypt: int = 512, pepper_length: int = 1
) -> str:
    """Legacy method, use encrypt_password instead"""
    return hash_password(password, salt, encrypt, pepper_length)


def generate_pepper(password: str, length: int = 1) -> str:
    """Legacy method, stop using this"""
    return "".join(choice(ascii_letters) for _ in range(length)) + password


def generate_form_token() -> str:
    """Legacy method, use generate_csrf_token instead"""
    return generate_csrf_token()


class Auth:
    @classmethod
    def is_email_address_valid(cls, email_address: str) -> bool:
        """Legacy class method, use from flask_imp.auth import is_email_address_valid instead"""
        return is_email_address_valid(email_address)

    @classmethod
    def is_username_valid(
        cls,
        username: str,
        allowed: t.Optional[t.List[t.Literal["all", "dot", "dash", "under"]]] = None,
    ) -> bool:
        """Legacy class method, use from flask_imp.auth import is_username_valid instead"""
        return is_username_valid(username, allowed)

    @classmethod
    def generate_csrf_token(cls) -> str:
        """Legacy class method, use from flask_imp.auth import generate_csrf_token instead"""
        return generate_csrf_token()

    @classmethod
    def generate_private_key(cls, hook: t.Optional[str]) -> str:
        """Legacy class method, use from flask_imp.auth import generate_private_key instead"""
        return generate_private_key(hook)

    @classmethod
    def generate_numeric_validator(cls, length: int) -> int:
        """Legacy class method, use from flask_imp.auth import generate_numeric_validator instead"""
        return generate_numeric_validator(length)

    @classmethod
    def generate_alphanumeric_validator(cls, length: int) -> str:
        """Legacy class method, use from flask_imp.auth import generate_alphanumeric_validator instead"""
        return generate_alphanumeric_validator(length)

    @classmethod
    def generate_email_validator(cls) -> str:
        """Legacy class method, use from flask_imp.auth import generate_private_key instead"""
        return generate_email_validator()

    @classmethod
    def generate_salt(cls, length: int = 4) -> str:
        """Legacy class method, use from flask_imp.auth import generate_salt instead"""
        return generate_salt(length)

    @classmethod
    def encrypt_password(
        cls,
        password: str,
        salt: str,
        encryption_level: int = 512,
        pepper_length: int = 1,
        pepper_position: t.Literal["start", "end"] = "end",
    ) -> str:
        """Legacy class method, use from flask_imp.auth import encrypt_password instead"""
        return encrypt_password(
            password, salt, encryption_level, pepper_length, pepper_position
        )

    @classmethod
    def authenticate_password(
        cls,
        input_password: str,
        database_password: str,
        database_salt: str,
        encryption_level: int = 512,
        pepper_length: int = 1,
        pepper_position: t.Literal["start", "end"] = "end",
    ) -> bool:
        """Legacy class method, use from flask_imp.auth import authenticate_password instead"""
        return authenticate_password(
            input_password,
            database_password,
            database_salt,
            encryption_level,
            pepper_length,
            pepper_position,
        )

    @classmethod
    def generate_password(cls, style: str = "mixed", length: int = 3) -> str:
        """Legacy class method, use from flask_imp.auth import generate_password instead"""
        return generate_password(style, length)

    # LEGACY METHODS

    @classmethod
    def auth_password(
        cls,
        input_password: str,
        database_password: str,
        database_salt: str,
        encrypt: int = 512,
        pepper_length: int = 1,
    ) -> bool:
        """Legacy class method, use from flask_imp.auth import authenticate_password instead"""
        return authenticate_password(
            input_password, database_password, database_salt, encrypt, pepper_length
        )

    @classmethod
    def hash_password(
        cls, password: str, salt: str, encrypt: int = 512, pepper_length: int = 1
    ) -> str:
        """Legacy class method, use from flask_imp.auth import encrypt_password instead"""
        return encrypt_password(password, salt, encrypt, pepper_length)

    @classmethod
    def sha_password(
        cls, password: str, salt: str, encrypt: int = 512, pepper_length: int = 1
    ) -> str:
        """Legacy class method, use from flask_imp.auth import encrypt_password instead"""
        return encrypt_password(password, salt, encrypt, pepper_length)

    @classmethod
    def generate_pepper(cls, password: str, length: int = 1) -> str:
        """Legacy class method, stop using this"""
        return "".join(choice(ascii_letters) for _ in range(length)) + password

    @classmethod
    def generate_form_token(cls) -> str:
        """Legacy class method, use from flask_imp.auth import generate_csrf_token instead"""
        return generate_csrf_token()
