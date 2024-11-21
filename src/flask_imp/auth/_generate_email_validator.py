from ._generate_alphanumeric_validator import generate_alphanumeric_validator


def generate_email_validator() -> str:
    """
    Uses generate_alphanumeric_validator with a length of 8 to
    generate a random alphanumeric value for the specific use of
    validating accounts via email.

    :return: alphanumeric of length 8
    """
    return str(generate_alphanumeric_validator(length=8))
