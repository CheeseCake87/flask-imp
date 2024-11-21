from random import randrange


def generate_numeric_validator(length: int) -> int:
    """
    Generates random choice between 1 * (length) and 9 * (length).

    Example return if length = 4: 5468

    For use in MFA email, or unique filename generation.

    :param length: length of number to generate
    :return: random integer of (length)
    """
    start = int("1" * length)
    end = int("9" * length)
    return randrange(start, end)
