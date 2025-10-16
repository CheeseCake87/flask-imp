import typing as t


def _check_against_values_allowed(
    session_value: t.Union[t.List[str], str, int, bool],
    values_allowed: t.Union[t.List[t.Union[str, int, bool]], str, int, bool],
) -> bool:
    """
    Checks if the session value matches the values allowed. Used by checkpoint.

    :param session_value: the value to check
    :param values_allowed: the value(s) to check against
    :return: True if the session value matches the values allowed, False otherwise
    """
    if isinstance(values_allowed, list):
        if isinstance(session_value, list):
            for value in session_value:
                if value in values_allowed:
                    return True
            return False

        if session_value in values_allowed:
            return True
        return False

    if session_value == values_allowed:
        return True

    return False
