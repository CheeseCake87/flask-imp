import typing as t
from hashlib import sha256, sha512


def _pps(pepper_: str, pass_: str, salt_: str) -> str:
    """
    Part of the private functions used in the password authentication process.

    Adds the pepper to the start of the password.

    :param pepper_: the pepper to add
    :param pass_: the password to add the pepper to
    :param salt_: the salt to add to the password
    :return: the password with the pepper added to the start
    """
    return pepper_ + pass_ + salt_


def _ppe(pepper_: str, pass_: str, salt_: str) -> str:
    """
    Part of the private functions used in the password authentication process.

    Adds the pepper to the end of the password.

    :param pepper_: the pepper to add
    :param pass_: the password to add the pepper to
    :param salt_: the salt to add to the password
    :return: the password with the pepper added to the end
    """
    return pass_ + pepper_ + salt_


def _guess_block(
    guesses: t.Set[str],
    input_password: str,
    database_password: str,
    database_salt: str,
    encryption_level: int = 512,
    pepper_position: t.Literal["start", "end"] = "end",
) -> bool:
    """
    Part of the private functions used in the password authentication process.

    Compares a set of guesses to a database password.

    :param guesses: a set of guesses to compare
    :param input_password: the input password
    :param database_password: the database password
    :param database_salt: the database salt
    :param encryption_level: the encryption level - defaults to 512
    :param pepper_position: the pepper position - defaults to "end"
    :return: True if a match is found, False otherwise
    """
    for guess in guesses:
        _sha = sha512() if encryption_level == 512 else sha256()
        _sha.update(
            (
                _pps(guess, input_password, database_salt)
                if pepper_position == "start"
                else _ppe(guess, input_password, database_salt)
            ).encode("utf-8")
        )
        if _sha.hexdigest() == database_password:
            return True

    return False
