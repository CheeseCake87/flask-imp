import re
import typing as t


def is_username_valid(
    username: str,
    allowed: t.Optional[t.List[t.Literal["all", "dot", "dash", "under"]]] = None,
) -> bool:
    """
    Checks if a username is valid.

    Valid usernames can only include letters,
    numbers, ., -, and _ but cannot begin or end with
    the last three mentioned.

    Example use::

        is_username_valid("username", allowed=["all"])

        Passes: username, user.name, user-name, user_name
        Fails: _user_name

        is_username_valid("username", allowed=["dot", "dash"])

        Passes: username, user.name, user-name, user-name.name
        Fails: user_name, _user_name, .user.name

    :param username: username to validate
    :param allowed: ["all", "dot", "dash", "under"] - defaults to ["all"]
    :return: True if username is valid, False otherwise
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
