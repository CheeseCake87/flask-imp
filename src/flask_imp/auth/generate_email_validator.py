from .generate_alphanumeric_validator import generate_alphanumeric_validator


def generate_email_validator() -> str:
    """
    Uses generate_numeric_validator with a length of 8 to
    generate a random number for the specific use of
    validating accounts via email.

    :raw-html:`<br />`

    See `generate_numeric_validator` for more information.

    :raw-html:`<br />`

    -----

    :return: str - number between 11111111 and 99999999
    """
    return str(generate_alphanumeric_validator(length=8))
