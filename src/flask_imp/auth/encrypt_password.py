import typing as t
from hashlib import sha256, sha512

from .__private_funcs__ import _attach_pepper


def encrypt_password(
        password: str,
        salt: str,
        encryption_level: int = 512,
        pepper_length: int = 1,
        pepper_position: t.Literal["start", "end"] = "end"
) -> str:
    """
    Takes the plain password, applies a pepper, salts it, then converts it to sha.

    :raw-html:`<br />`

    You will need to know the pepper length that the password was hashed wit

    :raw-html:`<br />`

    Can set the encryption level to 256 or 512.

    :raw-html:`<br />`

    For use in password hashing.

    :raw-html:`<br />`

    .. Note::

        pepper_length is capped at 3.

        You must inform the authenticate_password of the pepper length used to hash the password.

        You must inform the authenticate_password of the position of the pepper used to hash the password.

        You must inform the authenticate_password of the encryption level used to hash the password.

    :raw-html:`<br />`

    -----

    :param password: str - plain password
    :param salt: str - salt
    :param encryption_level: int - 256 or 512 - defaults to 512
    :param pepper_length: int - length of pepper
    :param pepper_position: str - "start" or "end" - defaults to "end"
    :return str: hash:
    """
    if pepper_length > 3:
        pepper_length = 3

    sha = sha512() if encryption_level == 512 else sha256()
    sha.update((_attach_pepper(password, pepper_length, pepper_position) + salt).encode("utf-8"))
    return sha.hexdigest()
