from functools import partial
from typing import Any, Optional

from flask import url_for

from ._utilities import LazySession


def lazy_url_for(
    endpoint: str,
    *,
    _anchor: Optional[str] = None,
    _method: Optional[str] = None,
    _scheme: Optional[str] = None,
    _external: Optional[bool] = None,
    **values: Any,
) -> partial[str]:
    """
    Indented for use in checkpoint decorators.

    Takes the same arguments as Flask's url_for function and loads url_for and the
    arguments passed to it into a partial to be run later.

    This allows url_for to be set outside of context and later ran inside context.

    `url_for` docstring:

    Generate a URL to the given endpoint with the given values.

    This requires an active request or application context, and calls
    :meth:`current_app.url_for() <flask.Flask.url_for>`. See that method
    for full documentation.

    :param endpoint: The endpoint name associated with the URL to
        generate. If this starts with a ``.``, the current blueprint
        name (if any) will be used.
    :param _anchor: If given, append this as ``#anchor`` to the URL.
    :param _method: If given, generate the URL associated with this
        method for the endpoint.
    :param _scheme: If given, the URL will have this scheme if it is
        external.
    :param _external: If given, prefer the URL to be internal (False) or
        require it to be external (True). External URLs include the
        scheme and domain. When not in an active request, URLs are
        external by default.
    :param values: Values to use for the variable parts of the URL rule.
        Unknown keys are appended as query string arguments, like
        ``?a=b&c=d``.
    """
    return partial(
        url_for,
        endpoint=endpoint,
        _scheme=_scheme,
        _anchor=_anchor,
        _method=_method,
        **values,
    )


def lazy_session_get(key: str, default: Any = None) -> LazySession:
    """
    Indented for use in checkpoint decorators.

    Returns a LazySession object that can be used to get a session
    value in checkpoint decorators.
    """

    return LazySession(key, default)


__all__ = [
    "lazy_url_for",
    "lazy_session_get",
]
