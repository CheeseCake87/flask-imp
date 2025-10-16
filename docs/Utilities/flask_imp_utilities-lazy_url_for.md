# lazy_url_for

```python
from flask_imp.utilities import lazy_url_for
```

```python
lazy_url_for(
    endpoint: str,
    *,
    _anchor: str | None = None,
    _method: str | None = None,
    _scheme: str | None = None,
    _external: bool | None = None,
    **values: Any
) -> partial[str]:
```

---

Indented for use in checkpoint decorators.

Takes the same arguments as Flask's url_for function and loads url_for and the
arguments passed to it into a partial to be run later.

This allows url_for to be set outside of context and later ran inside context.
