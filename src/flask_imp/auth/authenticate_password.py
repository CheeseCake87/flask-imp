import itertools
import typing as t
from hashlib import sha256, sha512
from string import ascii_letters


def authenticate_password(
        input_password: str,
        database_password: str,
        database_salt: str,
        encryption_level: int = 512,
        pepper_length: int = 1,
        pepper_position: t.Literal["start", "end"] = "end"
) -> bool:
    """
    Takes the plain input password, the stored hashed password along with the stored salt
    and will try every possible combination of pepper values to find a match.

    :raw-html:`<br />`

    .. Note::

        You must know the length of the pepper used to hash the password.

        You must know the position of the pepper used to hash the password.

        You must know the encryption level used to hash the password.

    :raw-html:`<br />`

    -----

    :param input_password: str - plain password
    :param database_password: str - hashed password from database
    :param database_salt: str - salt from database
    :param encryption_level: int - encryption used to generate database password
    :param pepper_length: int - length of pepper used to generate database password
    :param pepper_position: str - "start" or "end" - position of pepper used to generate database password
    :return: bool - True if match, False if not
    """

    if pepper_length > 3:
        pepper_length = 3

    _guesses = [''.join(i) for i in itertools.product(ascii_letters, repeat=pepper_length)]

    def _pps(pepper_, pass_, salt_) -> str:
        return pepper_ + pass_ + salt_

    def _ppe(pepper_, pass_, salt_) -> str:
        return pass_ + pepper_ + salt_

    for index, guess in enumerate(_guesses):
        _sha = sha512() if encryption_level == 512 else sha256()
        _sha.update(
            (_pps(
                guess, input_password, database_salt
            ) if pepper_position == "start" else _ppe(
                guess, input_password, database_salt
            )).encode("utf-8")
        )
        if _sha.hexdigest() == database_password:
            return True

    return False
