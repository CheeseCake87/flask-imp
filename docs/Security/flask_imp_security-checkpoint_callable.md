# checkpoint_callable

```python
from flask_imp.security import checkpoint_callable
```

```python
def checkpoint_callable(
    callable_: t.Callable[..., t.Any],
    predefined_args: t.Optional[t.Dict[str, t.Any]] = None,
    include_url_args: bool = False,
    fail_url: t.Optional[t.Union[str, t.Callable[[], t.Any]]] = None,
    fail_json: t.Optional[t.Dict[str, t.Any]] = None,
    fail_status: int = 403,
    pass_url: t.Optional[t.Union[str, t.Callable[[], t.Any]]] = None,
    message: t.Optional[str] = None,
    message_category: str = "message",
)
```

`@checkpoint_callable(...)`

---

A decorator that evaluates if the passed in callable is truly.

Useful for feature flags or other checks that need to be done before a route is accessed.

If `include_url_args` is set, the url variables of the route will be passed
into the callable as `__url_vars__` after any predefined_args.

*Example of using predefined_args*

```python
def check_if_number(value):
    if isinstance(value, int):
        if value > 10:
            return True
    return False


@bp.route("/number", methods=["GET"])
@checkpoint_callable(
    check_if_number,
    predefined_args={"value": os.getenv("NUMBER")},
    fail_url=lazy_url_for("www.index"),
    message="Failed message"
)
def number():
    ...
```

*Example of checking route variable*

```python
def check_url_vars(__url_vars__):
    if __url_vars__["value"] == 10:
        return True
    return False


...


@bp.route("/number/<int:value>", methods=["GET"])
@checkpoint_callable(
    check_url_vars,
    include_url_args=True,
    fail_url=lazy_url_for("wrong_number"),
    message="Failed message"
)
def number():
    ...
```

*Example of using predefined_args from session*

```python
def check_session_vars(value):
    # lazy_session_get is evaluated in the decorator.
    if value == 10:
        return True
    return False


...


@bp.route("/number", methods=["GET"])
@checkpoint_callable(
    check_session_vars,
    predefined_args={"value": lazy_session_get("NUMBER")},
    fail_url=lazy_url_for("www.index"),
    message="Failed message"
)
def number():
    ...
```
