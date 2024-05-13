```
Menu = Blueprint.x/init_session
Title = Blueprint.init_session
```

```python
init_session() -> None
```

---

Has the same functionality as [Imp.x / init_session](imp_x-init_session.html) but loads session key values from the
Blueprint's config file.

```python
@bp.before_app_request
def before_app_request():
    bp.init_session()
```