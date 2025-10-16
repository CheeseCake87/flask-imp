# BearerCheckpoint

```python
from flask_imp.security import BearerCheckpoint
```

```python
BearerCheckpoint(
    token: str,
).action(
    fail_url: t.Optional[t.Union[str | partial]] = None,
    fail_json: t.Optional[t.Dict[str, t.Any]] = None,
    fail_status: int = 403,
    pass_url: t.Optional[t.Union[str | partial]] = None,
    message: t.Optional[str] = None,
    message_category: str = "message"
)
```

---

A checkpoint that checks if the authorization header is of type Bearer,
and that the token in the request is valid.

`token` The token to check for.

`.action(...)`:

`fail_url` The url to redirect to if the key value fails.

`fail_json` JSON that is returned on failure.

`fail_status` The status code to return if the check fails, defaults to `403`.

`pass_url` The url to redirect to if the key value passes.

`message` If a message is specified, a flash message is shown.

`message_category` The category of the flash message.

If fail_json is provided, passing to endpoints will be disabled.

`pass_url` and `fail_url` take either a string or the `utilities.lazy_url_for` function.

**Examples:**

```python
BEARER_REQ = BearerCheckpoint("hello,world").action(fail_json={"error": "token"})


@bp.route("/admin", methods=["GET"])
@checkpoint(BEARER_REQ)
def admin_page():
    ...
```
