# SQLDatabaseConfig

```python
from flask_imp.config import SQLDatabaseConfig
```

```python
SQLDatabaseConfig(
    dialect: t.Literal["mysql", "postgresql", "oracle", "mssql"],
    database_name: str,
    location: str,
    port: int,
    username: str,
    password: str,
    bind_key: t.Optional[str] = None,
    enabled: bool = True,
)
```

---

A class that holds a SQL database configuration.

This configuration is parsed into a database URI and
used in either the `SQLALCHEMY_DATABASE_URI` or `SQLALCHEMY_BINDS` configuration variables.

