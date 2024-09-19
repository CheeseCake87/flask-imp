from random import choice
from string import punctuation


def generate_salt(length: int = 4) -> str:
    """
    Generates a string of (length) characters of punctuation.

    :raw-html:`<br />`

    The Default length is 4.

    :raw-html:`<br />`

    For use in password salting

    :raw-html:`<br />`

    -----

    :return: str - salt of (length)
    """
    return "".join(choice(punctuation) for _ in range(length))
