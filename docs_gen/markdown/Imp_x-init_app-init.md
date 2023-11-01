```
Menu = Imp.x/init_app, __init__
Title = Imp.init_app, __init__
```

```python
init_app(
    app: Flask,
    app_config_file: Optional[str] = None,
    ignore_missing_env_variables: bool = False
) -> None
# -or- 
Imp(
    app: Optional[Flask] = None,
    app_config_file: Optional[str] = None,
    ignore_missing_env_variables: bool = False
) -> None
```

---

Initializes the flask app to work with flask-imp.

If no `app_config_file` specified, an attempt to read `IMP_CONFIG` from the environment will be made.

If `IMP_CONFIG` is not in the environment variables, an attempt to load `default.config.toml` will be made.

`default.config.toml` will be created, and used if not found.

If `ignore_missing_env_variables` is `True`, then missing environment variables will be ignored.

If `ignore_missing_env_variables` is `False` (default), then missing environment variables will raise a ValueError

