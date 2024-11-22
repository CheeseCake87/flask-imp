# SQLiteDatabaseConfig

```python
from flask_imp.config import SQLiteDatabaseConfig
```

```python
SQLiteDatabaseConfig(
    enabled: bool = True,
    name: str = "database",
    bind_key: str = "",
    sqlite_db_extension: str = ".sqlite",
    location: t.Optional[Path] = None,
)
```

---

A class that holds a SQLite database configuration.

This configuration is parsed into a database URI and
used in either the `SQLALCHEMY_DATABASE_URI` or `SQLALCHEMY_BINDS` configuration variables.
