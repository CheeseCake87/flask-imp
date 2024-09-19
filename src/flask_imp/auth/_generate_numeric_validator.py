from random import randrange


def generate_numeric_validator(length: int) -> int:
    """
    Generates random choice between 1 * (length) and 9 * (length).

    :raw-html:`<br />`

    If the length is 4, it will generate a number between 1111 and 9999.

    :raw-html:`<br />`

    For use in MFA email, or unique filename generation.

    :raw-html:`<br />`

    -----
    :param length: int - length of number to generate
    :return: int - Example return of number between 1111 and 9999 if length is 4
    """
    start = int("1" * length)
    end = int("9" * length)
    return randrange(start, end)
