# DatabaseConfig

```python
from flask_imp.config import DatabaseConfig
```

```python
DatabaseConfig(
    enabled: bool = False,
    dialect: t.Literal[
        "mysql", "postgresql", "sqlite", "oracle", "mssql"
    ] = "sqlite",
    name: str = "database",
    bind_key: str = "",
    location: str = "",
    port: int = 0,
    username: str = "",
    password: str = "",
    sqlite_db_extension: str = ".sqlite"
)
```

---

A class that holds a database configuration.

This configuration is parsed into a database URI and
used in either the `SQLALCHEMY_DATABASE_URI` or `SQLALCHEMY_BINDS` configuration variables.
