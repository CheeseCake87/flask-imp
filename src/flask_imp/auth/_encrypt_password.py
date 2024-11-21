import typing as t
from hashlib import sha256, sha512
from random import choice
from string import ascii_letters

from ._private_funcs import _pps, _ppe


def encrypt_password(
    password: str,
    salt: str,
    encryption_level: int = 512,
    pepper_length: int = 1,
    pepper_position: t.Literal["start", "end"] = "end",
) -> str:
    """
    Takes the plain password, applies a pepper, salts it, then produces a digested sha512 or sha256 if specified.

    - Can set the encryption level to 256 or 512, defaults to 512.
    - Can set the pepper length, defaults to 1. Max is 3.
    - Can set the pepper position, "start" or "end", defaults to "end".

    For use in password hashing.

    You must inform the authenticate_password function of:

    - the pepper length used to hash the password.
    - the position of the pepper used to hash the password.
    - the encryption level used to hash the password.

    :param password: str - plain password
    :param salt: str - salt
    :param encryption_level: int - 256 or 512 - defaults to 512
    :param pepper_length: int - length of pepper
    :param pepper_position: str - "start" or "end" - defaults to "end"
    :return str: hash:
    """

    if pepper_length > 3:
        pepper_length = 3

    _sha = sha512() if encryption_level == 512 else sha256()
    _pepper = "".join(choice(ascii_letters) for _ in range(pepper_length))

    _sha.update(
        (
            _pps(_pepper, password, salt)
            if pepper_position == "start"
            else _ppe(_pepper, password, salt)
        ).encode("utf-8")
    )
    return _sha.hexdigest()
