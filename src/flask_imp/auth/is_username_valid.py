import re
import typing as t


def is_username_valid(
    username: str,
    allowed: t.Optional[t.List[t.Literal["all", "dot", "dash", "under"]]] = None,
) -> bool:
    """
    Checks if a username is valid.

    :raw-html:`<br />`

    Valid usernames can only include letters,
    numbers, ., -, and _ but cannot begin or end with
    the last three mentioned.

    :raw-html:`<br />`


    **Example use:**

    :raw-html:`<br />`

    .. code-block::

            is_username_valid("username", allowed=["all"])

    :raw-html:`<br />`

    **Output:**

    .. code-block::

        username : WILL PASS : True
        user.name : WILL PASS : True
        user-name : WILL PASS : True
        user_name : WILL PASS : True
        _user_name : WILL PASS : False


    :raw-html:`<br />`

    .. code-block::

            is_username_valid("username", allowed=["dot", "dash"])

    :raw-html:`<br />`

    **Output:**

    .. code-block::

        username : WILL PASS : True
        user.name : WILL PASS : True
        user-name : WILL PASS : True
        user-name.name : WILL PASS : True
        user_name : WILL PASS : False
        _user_name : WILL PASS : False
        .user.name : WILL PASS : False

    :raw-html:`<br />`

    -----

    :param username: str
    :param allowed: list - ["all", "dot", "dash", "under"] - defaults to ["all"]
    :return bool:
    """

    if not username[0].isalnum() or not username[-1].isalnum():
        return False

    if allowed is None:
        allowed = ["all"]

    if "all" in allowed:
        return bool(re.match(r"^[a-zA-Z0-9._-]+$", username))

    if "under" not in allowed:
        if "_" in username:
            return False

    if "dot" not in allowed:
        if "." in username:
            return False

    if "dash" not in allowed:
        if "-" in username:
            return False

    return True
