import typing as t
from random import choice
from string import ascii_letters


def _attach_pepper(password: str, length: int = 1, position: t.Literal["start", "end"] = "end") -> str:
    """
    Chooses a random letter from ascii_letters and joins it onto the user's password,
    this is used to pepper the password.

    :raw-html:`<br />`

    You can increase the length of the pepper by passing in a length value.
    This will add to the complexity of password guessing when using the auth_password method.

    :raw-html:`<br />`

    You can set the position of the pepper by passing in a position value "start" or "end" defaults to "end".

    :raw-html:`<br />`

    .. Note::

        length is capped at 3.

    :raw-html:`<br />`

    -----

    :param password: str - user's password
    :param length: int - length of pepper - defaults to 1, capped at 3
    :param position: str - "start" or "end" - defaults to "end"
    :return: str - peppered password
    """
    if length > 3:
        length = 3

    if position == "start":
        return password + "".join(choice(ascii_letters) for _ in range(length))

    return "".join(choice(ascii_letters) for _ in range(length)) + password
