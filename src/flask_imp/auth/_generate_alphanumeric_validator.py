from random import choice
from string import ascii_uppercase, digits


def generate_alphanumeric_validator(length: int) -> str:
    """
    Generates (length) of alphanumeric.

    For use in MFA email, or unique filename generation.

    Example return of "F5R6" if length is 4

    :param length: length of alphanumeric to generate
    :return: alphanumeric of length (length)
    """

    _alpha_numeric = ascii_uppercase + digits
    return "".join([choice(_alpha_numeric) for _ in range(length)])
