# DatabaseConfig

```python
from flask_imp.config import DatabaseConfig
```

```python
DatabaseConfig(
    dialect: t.Literal[
        "mysql", "postgresql", "sqlite", "oracle", "mssql"
    ] = "sqlite",
    database_name: str = "database",
    location: str = "",
    port: int = 0,
    username: str = "",
    password: str = "",
    sqlite_db_extension: str = ".sqlite",
    bind_key: t.Optional[str] = None,
    enabled: bool = True,
)
```

---

A class that holds a database configuration.

This configuration is parsed into a database URI and
used in either the `SQLALCHEMY_DATABASE_URI` or `SQLALCHEMY_BINDS` configuration variables.

