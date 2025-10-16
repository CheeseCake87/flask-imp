# checkpoint

```python
from flask_imp.security import checkpoint
```

```python
checkpoint(
    checkpoint_: t.Union[APIKeyCheckpoint, BearerCheckpoint, SessionCheckpoint]
)
```

`@checkpoint(...)`

---

A decorator that checks if the specified checkpoint will pass or fail.

`checkpoint_` The checkpoint class to pass or fail.

**Example of a route that requires a user to be logged in:**

```python
from flask_imp.security import checkpoint, SessionCheckpoint
from flask_imp.utilities import lazy_url_for

...

LOG_IN_REQ = SessionCheckpoint(
    session_key="logged_in",
    values_allowed=True,
).action(
    fail_url=lazy_url_for("login")  # If logged_in is False, this will trigger
)


@bp.route("/admin", methods=["GET"])
@checkpoint(LOG_IN_REQ)
def admin_page():
    ...
```

**Example of multiple checks:**

```python
LOG_IN_REQ = SessionCheckpoint(
    session_key="logged_in",
    values_allowed=True,
).action(
    fail_url=lazy_url_for("blueprint.login_page"),
    message="Login needed"  # This will set Flask's flash message
)

ADMIN_PERM = SessionCheckpoint(
    session_key="user_type",
    values_allowed="admin",
).action(
    fail_url=lazy_url_for("blueprint.index"),
    message="You need to be an admin to access this page"
)


@bp.route("/admin", methods=["GET"])
@checkpoint(LOG_IN_REQ)
@checkpoint(ADMIN_PERM)
def admin_page():
    ...
```

**Example of a route that if the user is already logged in, redirects to the specified endpoint:**

```python
IS_LOGGED_IN = SessionCheckpoint(
    session_key='logged_in',
    values_allowed=True,
).action(
    pass_endpoint='blueprint.admin_page',
    message="Already logged in"
)


@bp.route("/login-page", methods=["GET"])
@checkpoint(IS_LOGGED_IN)
def login_page():
    ...
```

