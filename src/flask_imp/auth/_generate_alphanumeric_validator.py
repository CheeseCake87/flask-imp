from random import choice
from string import ascii_uppercase, digits


def generate_alphanumeric_validator(length: int) -> str:
    """
    Generates (length) of alphanumeric.

    :raw-html:`<br />`

    For use in MFA email, or unique filename generation.

    :raw-html:`<br />`

    -----
    :param length: int - length of alphanumeric to generate
    :return: str - Example return of "F5R6" if length is 4
    """

    _alpha_numeric = ascii_uppercase + digits
    return "".join([choice(_alpha_numeric) for _ in range(length)])
