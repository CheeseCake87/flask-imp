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
    function: t.Callable[..., t.Any],
    predefined_args: t.Optional[t.Dict[str, t.Any]] = None,
    fail_endpoint: t.Optional[str] = None,
    pass_endpoint: t.Optional[str] = None,
    endpoint_kwargs: t.Optional[t.Dict[str, t.Union[str, int]]] = None,
    message: t.Optional[str] = None,
    message_category: str = "message",
    fail_on_missing_kwargs: bool = False,
    abort_status: int = 403,
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
        if value > 10:
            return True
    return False

# This will check if the URL variable 'value' is an integer and greater than 10
@bp.route("/number/<int:value>", methods=["GET"])
@pass_function_check(
    check_if_number,
    fail_endpoint="wrong_number",
    message="Failed message"
)
def number():
    ...

# This will check if an environment variable 'value' is an integer and greater than 10
@bp.route("/number", methods=["GET"])
@pass_function_check(
    check_if_number,
    predefined_args={"value": os.getenv("NUMBER")},
    fail_endpoint="www.index",
    message="Failed message"
)
def number():
    ...
```
