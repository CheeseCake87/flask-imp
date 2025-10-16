# APIKeyCheckpoint

```python
from flask_imp.security import APIKeyCheckpoint
```

```python
APIKeyCheckpoint(
    key: str,
    type_: t.Literal["header", "query_param"] = "header",
    header_or_param: str = "x-api-key",
).action(
    fail_url: t.Optional[t.Union[str, t.Callable[[], t.Any]]] = None,
    fail_json: t.Optional[t.Dict[str, t.Any]] = None,
    fail_status: int = 403,
    pass_url: t.Optional[t.Union[str, t.Callable[[], t.Any]]] = None,
    message: t.Optional[str] = None,
    message_category: str = "message",
)
```

---

A checkpoint that checks if the specified header or query parameter exists, and that
the key in the request is valid.

`key` The key to validate against.

`type_` Where to look for the key.

`header_or_param` What header or query param value will the key be expected.

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

This will look for the `x-api-key` key in the request header, and match it to the value
of `hello`:

```python
API_KEY_HEADER = APIKeyCheckpoint("hello")

@bp.route("/admin", methods=["GET"])
@checkpoint(API_KEY_HEADER)
def admin_page():
    ...
```

This will do the same check as above but look in the url params instead:

`https://example.com/admin?x-api-key=hello`

```python
API_KEY_QUERY_PARAM = APIKeyCheckpoint("hello", type_="query_param")

@bp.route("/admin", methods=["GET"])
@checkpoint(API_KEY_QUERY_PARAM)
def admin_page():
    ...
```

This will send JSON if the key is invalid:

```python
API_KEY_HEADER = APIKeyCheckpoint("hello").action(fail_json={"error": "invalid key"})

@bp.route("/admin", methods=["GET"])
@checkpoint(API_KEY_HEADER)
def admin_page():
    ...
```
