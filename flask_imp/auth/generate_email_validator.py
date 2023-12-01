from .generate_alphanumeric_validator import generate_alphanumeric_validator


def generate_email_validator() -> str:
    """
    Uses generate_alphanumeric_validator with a length of 8 to
    generate a random alphanumeric value for the specific use of
    validating accounts via email.

    :raw-html:`<br />`

    See `generate_alphanumeric_validator` for more information.

    :raw-html:`<br />`

    -----

    :return: str - alphanumeric of length 8
    """
    return str(generate_alphanumeric_validator(length=8))
