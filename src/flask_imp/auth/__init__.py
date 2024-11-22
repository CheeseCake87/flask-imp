"""
This module contains the authentication utilities for a Flask application.

Functions:

    - authenticate_password: Authenticates a password against a hashed password.
    - encrypt_password: Encrypts a password with a salt and pepper.
    - generate_alphanumeric_validator: Generates a validator for alphanumeric strings.
    - generate_csrf_token: Generates a CSRF token.
    - generate_email_validator: Generates a validator for email addresses.
    - generate_numeric_validator: Generates a validator for numeric strings.
    - generate_password: Generates a password.
    - generate_private_key: Generates a private key.
    - generate_salt: Generates a salt.
    - is_email_address_valid: Validates an email address.
    - is_username_valid: Validates a username.
"""

from ._authenticate_password import authenticate_password
from ._encrypt_password import encrypt_password
from ._generate_alphanumeric_validator import generate_alphanumeric_validator
from ._generate_csrf_token import generate_csrf_token
from ._generate_email_validator import generate_email_validator
from ._generate_numeric_validator import generate_numeric_validator
from ._generate_password import generate_password
from ._generate_private_key import generate_private_key
from ._generate_salt import generate_salt
from ._is_email_address_valid import is_email_address_valid
from ._is_username_valid import is_username_valid

__all__ = [
    "is_email_address_valid",
    "is_username_valid",
    "generate_csrf_token",
    "generate_private_key",
    "generate_numeric_validator",
    "generate_alphanumeric_validator",
    "generate_email_validator",
    "generate_salt",
    "encrypt_password",
    "authenticate_password",
    "generate_password",
]
