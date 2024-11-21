from random import choice
from typing import Literal

from ._dataclasses import PasswordGeneration
from ._generate_numeric_validator import generate_numeric_validator


def generate_password(
    style: Literal["animals", "colors", "mixed"] = "mixed", length: int = 3
) -> str:
    """
    Generates a plain text password based on choice of style and length.

    (length) of random numbers are appended to the end of every generated password.

    style options: "animals", "colors", "mixed" - defaults to "mixed"

    :param style: "animals", "colors", "mixed" - defaults to "mixed"
    :param length: the number of words joined - defaults to 3
    :return: a generated password
    """
    if style == "animals":
        return "-".join(
            [choice(PasswordGeneration.animals) for _ in range(length)]
        ) + str(generate_numeric_validator(length=length))

    if style == "colors":
        return "-".join(
            [choice(PasswordGeneration.colors) for _ in range(length)]
        ) + str(generate_numeric_validator(length=length))

    if style == "mixed":
        return "-".join(
            [
                choice([*PasswordGeneration.animals, *PasswordGeneration.colors])
                for _ in range(length)
            ]
        ) + str(generate_numeric_validator(length=length))

    raise ValueError(f"Invalid style passed in {style}")
