```
Menu = flask_imp.security/include_csrf
Title = include_csrf - flask_imp.security
```

```python
from flask_imp.security import include_csrf
```

```python
include_csrf(
    session_key: str = "csrf",
    form_key: str = "csrf",
    abort_code: int = 401
)
```

`@include_csrf(...)`

---


A decorator that handles CSRF protection.

On a **GET** request, a CSRF token is generated and stored in the session key
specified by the session_key parameter.

On a **POST** request, the form_key specified is checked against the session_key
specified.

- If they match, the request is allowed to continue.
- If no match, the response will be abort(abort_code), default 401.

```python
@bp.route("/admin", methods=["GET", "POST"])
@include_csrf(session_key="csrf", form_key="csrf")
def admin_page():
    ...
    # You must pass in the CSRF token from the session into the template.
    # Then add <input type="hidden" name="csrf" value="{{ csrf }}"> to the form.
    return render_template("admin.html", csrf=session.get("csrf"))
```

Form key:

```html
<input type="hidden" name="csrf" value="{{ csrf }}">
```