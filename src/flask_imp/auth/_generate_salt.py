from random import choice
from string import punctuation


def generate_salt(length: int = 4) -> str:
    """
    Generates a string of (length) characters of punctuation.

    The Default length is 4.

    For use in password salting

    :return: a salt of (length)
    """
    return "".join(choice(punctuation) for _ in range(length))
