import typing as t
from hashlib import sha256, sha512


def _pps(pepper_, pass_, salt_) -> str:
    return pepper_ + pass_ + salt_


def _ppe(pepper_, pass_, salt_) -> str:
    return pass_ + pepper_ + salt_


def _guess_block(
    guesses: set,
    input_password: str,
    database_password: str,
    database_salt: str,
    encryption_level: int = 512,
    pepper_position: t.Literal["start", "end"] = "end",
) -> bool:
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
