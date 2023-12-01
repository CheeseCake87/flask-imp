from random import choice

from .dataclasses import PasswordGeneration
from .generate_numeric_validator import generate_numeric_validator


def generate_password(style: str = "mixed", length: int = 3) -> str:
    """
    Generates a plain text password based on choice of style and length.
    2 random numbers are appended to the end of every generated password.

    :raw-html:`<br />`

    style options: "animals", "colors", "mixed" - defaults to "mixed"

    :raw-html:`<br />`

    **Example use:**

    .. code-block::

        generate_password(style="animals", length=3)

    :raw-html:`<br />`

    **Output:**

    Cat-Goat-Pig12

    :raw-html:`<br />`

    -----

    :param style: str - "animals", "colors", "mixed" - defaults to "mixed"
    :param length: int - how many words are chosen - defaults to 3
    :return: str - a generated plain text password
    """
    if style == "animals":
        return "-".join(
            [choice(PasswordGeneration.animals) for _ in range(length)]
        ) + str(generate_numeric_validator(length=2))

    if style == "colors":
        return "-".join(
            [choice(PasswordGeneration.colors) for _ in range(length)]
        ) + str(generate_numeric_validator(length=2))

    if style == "mixed":
        return "-".join(
            [
                choice([*PasswordGeneration.animals, *PasswordGeneration.colors])
                for _ in range(length)
            ]
        ) + str(generate_numeric_validator(length=2))

    raise ValueError(f"Invalid style passed in {style}")
