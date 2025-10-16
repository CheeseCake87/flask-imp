# SessionCheckpoint

```python
from flask_imp.security import SessionCheckpoint
```

```python
SessionCheckpoint(
    session_key: str,
    values_allowed: t.Union[t.List[t.Union[str, int, bool]], str, int, bool],
).action(
    pass_url: t.Optional[t.Union[str | partial]] = None,
    fail_url: t.Optional[t.Union[str | partial]] = None,
    fail_json: t.Optional[t.Dict[str, t.Any]] = None,
    fail_status: int = 403,
    message: t.Optional[str] = None,
    message_category: str = "message"
)
```

---

A checkpoint that checks if the specified session key exists and its value(s) match the specified value(s).

`session_key` The session key to check for.

`values_allowed` A list of or singular value(s) that the session key must contain.

`.action(...)`:

`pass_url` The url to redirect to if the key value passes.

`fail_url` The url to redirect to if the key value fails.

`fail_json` JSON that is returned on failure.

`fail_status` The status code to return if the check fails, defaults to `403`.

`message` If a message is specified, a flash message is shown.

`message_category` The category of the flash message.

If fail_json is provided, passing to endpoints will be disabled.

`pass_url` and `fail_url` take either a string or the `utilities.lazy_url_for` function.

**Examples:**

```python
@bp.route("/admin", methods=["GET"])
@checkpoint(
    SessionCheckpoint(
        "logged_in", True
    ).action(
        lazy_url_for("login_page"),
        message="Login required for this page!"
    )
)
def admin_page():
    ...
```

**Example of multiple checks:**

```python
@bp.route("/admin", methods=["GET"])
@checkpoint(
    SessionCheckpoint(
        "logged_in", True
    ).action(
        lazy_url_for("login_page"),
        message="Login required for this page!"
    )
)
@checkpoint(
    SessionCheckpoint(
        "user_type", "admin"
    ).action(
        lazy_url_for("index"),
        message="You need to be an admin to access this page!"
    )
)
def admin_page():
    ...
```

**Example of a route that if the user is already logged in, redirects to the specified endpoint:**

```python
@bp.route("/login-page", methods=["GET"])
@checkpoint(
    SessionCheckpoint(
        "logged_in", True
    ).action(
        pass_url=lazy_url_for("dashboard"),
        message="you are already logged in!"
    )
)
def login_page():
    ...
```
