# lazy_session_get

```python
from flask_imp.utilities import lazy_session_get
```

```python
lazy_session_get(key, default=None) -> LazySession:
```

---

Indented for use in checkpoint decorators.

Returns a LazySession object that can be used to evaluate a session
value in checkpoint decorators.
