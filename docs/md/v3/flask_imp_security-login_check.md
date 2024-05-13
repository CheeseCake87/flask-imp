```
Menu = flask_imp.security/login_check
Title = login_check - flask_imp.security
```

```python
from flask_imp.security import login_check
```

```python
login_check(
    session_key: str,
    values_allowed: t.Union[t.List[t.Union[str, int, bool]], str, int, bool],
    fail_endpoint: t.Optional[str] = None,
    pass_endpoint: t.Optional[str] = None,
    endpoint_kwargs: t.Optional[t.Dict[str, t.Union[str, int]]] = None,
    message: t.Optional[str] = None,
    message_category: str = "message"
)
```

`@login_check(...)`

---

A decorator that checks if the specified session key exists and contains the specified value.

`session_key` The session key to check for.

`values_allowed` A list of or singular value(s) that the session key must contain.

`fail_endpoint` The endpoint to redirect to if the session key does not exist or does not contain the specified values.

`endpoint_kwargs` A dictionary of keyword arguments to pass to the redirect endpoint.

`message` If a message is specified, a flash message is shown.

`message_category` The category of the flash message.

##### Example of a route that requires a user to be logged in:

```python
@bp.route("/admin", methods=["GET"])
@login_check(
    'logged_in',
    True,
    fail_endpoint='blueprint.login_page',
    message="Login needed"
)
def admin_page():
    ...
```

##### Example of a route that if the user is already logged in, redirects to the specified endpoint:

```python
@bp.route("/login-page", methods=["GET"])
@login_check(
    'logged_in',
    True,
    pass_endpoint='blueprint.admin_page',
    message="Already logged in"
)
def login_page():
    ...
```
