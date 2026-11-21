import warnings
from random import choice
from string import punctuation


def generate_salt(length: int = 4) -> str:
    """
    .. deprecated:: 6.5.0
        Argon2id generates and stores its own salt, see flask_imp.auth.hash_password.
        This function will be removed in a future version.

    Generates a string of (length) characters of punctuation.

    The Default length is 4.

    For use in password salting

    :return: a salt of (length)
    """
    warnings.warn(
        "generate_salt is deprecated and will be removed in a future version. "
        "flask_imp.auth.hash_password generates and stores its own salt.",
        DeprecationWarning,
        stacklevel=2,
    )
    return "".join(choice(punctuation) for _ in range(length))
