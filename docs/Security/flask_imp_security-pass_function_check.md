# pass_function_check

```
Menu = flask_imp.security/pass_function_check
Title = pass_function_check
```

```python
from flask_imp.security import pass_function_check
```

```python
def pass_function_check(
    function: t.Callable,
    predefined_args: t.Optional[t.Dict] = None,
    fail_endpoint: t.Optional[str] = None,
    pass_endpoint: t.Optional[str] = None,
    endpoint_kwargs: t.Optional[t.Dict[str, t.Union[str, int]]] = None,
    message: t.Optional[str] = None,
    message_category: str = "message",
    fail_on_missing_kwargs: bool = False,
    with_app_context: bool = False,
)
```

**NOTE: This was added mostly as an experimental feature, but ended up being useful in some cases.**

A decorator that takes the result of a function and checks if it is True or False.

URL variables from `@route` will be read by this decorator.
To use URL variables in your passed in function,
make sure your functions argument(s) name(s) match the name(s) of the URL variable(s).

**Example:**

```python
def check_if_number(value):
    if isinstance(value, int):
        return True
    return False

@bp.route("/admin-page/<int:value>", methods=["GET"])
@login_check('logged_in', True, 'blueprint.login_page')  # can be mixed with login_check
@pass_function_check(
    check_if_number,
    predefined_args=None,
    fail_endpoint='www.index',
    message="Failed message"
)
def admin_page():
    ...

@bp.route("/admin-page/<int:value>", methods=["GET"])
@login_check('logged_in', True, 'blueprint.login_page')  # can be mixed with login_check
@pass_function_check(
    check_if_number,
    predefined_args={'value': 10},
    fail_endpoint='www.index',
    message="Failed message"
)
def admin_page_overwrite():
    ...
```

**Advanced use case:**

Here's an example of accessing flask.session from within the passed in function. including the
`with_app_context` parameter, the function will be called with `app_context()`.

```python
from flask import current_app
from flask import session

...

def check_if_number(number=1, session_=None):
    if session_:
        print(session_)
    try:
        int(number)
        return True
    except ValueError:
        return False

@bp.route("/pass-func-check-with-url-var/<number>", methods=["GET"])
@pass_function_check(
    check_if_number,
    predefined_args={'number': 10, 'session_': session},
    fail_endpoint="www.index",
    with_app_context=True
)
def admin_page_overwrite_with_session():
    ...
```

If you pass in a predefined arg that has the same key name as a session variable that exists, the value
of that predefined arg will be replaced with the session variable value.

```python
session['car'] = 'Toyota'
...
def check_function(car):
    if car == 'Toyota':
        return True
    return False
...
@bp.route("/pass-func-check-with-url-var/<number>", methods=["GET"])
@pass_function_check(
    check_function,
    predefined_args={'car': session},
    ...

```

This will pass, as pass_function_check will replace the value of the predefined arg 'car' with the value
of the session variable 'car'.
