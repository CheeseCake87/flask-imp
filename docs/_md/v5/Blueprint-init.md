```
Menu = Blueprint.x/__init__
Title = Flask-Imp Blueprint __init__
```

```python
Blueprint(dunder_name: str, config_file: str = "config.toml") -> None
```

---

Initializes the Flask-Imp Blueprint.

`dunder_name` should always be set to `__name__`

`config_file` is the name of the config file to load.
It will be loaded from the same directory as the `__init__.py` file.
