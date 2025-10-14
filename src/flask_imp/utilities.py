from functools import partial
from typing import Any

from flask import url_for


def lazy_url_for(
    endpoint: str,
    *,
    _anchor: str | None = None,
    _method: str | None = None,
    _scheme: str | None = None,
    _external: bool | None = None,
    **values: Any,
):
    return partial(
        url_for,
        endpoint=endpoint,
        _scheme=_scheme,
        _anchor=_anchor,
        _method=_method,
        **values,
    )
