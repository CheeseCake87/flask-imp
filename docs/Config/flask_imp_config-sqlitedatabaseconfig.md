# SQLiteDatabaseConfig

```python
from flask_imp.config import SQLiteDatabaseConfig
```

```python
SQLiteDatabaseConfig(
    database_name: str = "database",
    sqlite_db_extension: str = ".sqlite",
    location: t.Optional[Path] = None,
    bind_key: t.Optional[str] = None,
    enabled: bool = True,
)
```

---

A class that holds a SQLite database configuration.

This configuration is parsed into a database URI and
used in either the `SQLALCHEMY_DATABASE_URI` or `SQLALCHEMY_BINDS` configuration variables.

