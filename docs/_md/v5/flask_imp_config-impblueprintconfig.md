```
Menu = flask_imp.config/ImpBlueprintConfig
Title = ImpBlueprintConfig - flask_imp.config
```

```python
from flask_imp.config import ImpBlueprintConfig
```

```python
ImpBlueprintConfig(
    enabled: bool = False,
    url_prefix: str = None,
    subdomain: str = None,
    url_defaults: dict = None,
    static_folder: str = "static",
    template_folder: str = "templates",
    static_url_path: str = "/static",
    root_path: str = None,
    cli_group: str = None,
    init_session: dict = None,
    database_binds: t.Iterable[DatabaseConfig] = None
)
```

---

A class that holds a Flask-Imp blueprint configuration.

Most of these values are passed to the `Blueprint` class when the blueprint is registered.

The `enabled` argument is used to enable or disable the blueprint. This is useful for feature flags.

`init_session` is used to set the session values in the main `before_request` function.

`database_binds` is a list of `DatabaseConfig` instances that are used to create `SQLALCHEMY_BINDS` configuration
variables. Again this is useful for feature flags, or for creating multiple databases per blueprint.