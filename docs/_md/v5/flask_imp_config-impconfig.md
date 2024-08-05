```
Menu = flask_imp.config/ImpConfig
Title = ImpConfig - flask_imp.config
```

```python
from flask_imp.config import ImpConfig
```

```python
ImpConfig(
    init_session: dict = None,
    database_main: t.Optional[DatabaseConfig] = None,
    database_binds: t.Optional[list[DatabaseConfig]] = None
)
```

---

The `ImpConfig` class is used to set the initial session, the main database, and any additional databases 
that the application will use.

```python
imp_config = ImpConfig(
    init_session={"key": "value"},
    database_main=DatabaseConfig(
        enabled=True,
        dialect="sqlite",
        name="test1",
    ),
    database_binds=[
        DatabaseConfig(
            enabled=True,
            dialect="sqlite",
            name="test2",
            bind_key="test2"
        )
    ]
)


def create_app():
    app = Flask(__name__)
    FlaskConfig(debug=True, app_instance=app)
    imp.init_app(app, imp_config)
    ...
```