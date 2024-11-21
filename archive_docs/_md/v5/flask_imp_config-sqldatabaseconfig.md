```
Menu = flask_imp.config/SQLDatabaseConfig
Title = SQLDatabaseConfig - flask_imp.config
```

```python
from flask_imp.config import SQLDatabaseConfig
```

```python
SQLDatabaseConfig(
    dialect: t.Literal["mysql", "postgresql", "oracle", "mssql"],
    enabled: bool = True,
    name: str = "database",
    bind_key: str = "",
    location: str = "",
    port: int = 0,
    username: str = "",
    password: str = "",
)
```

---

A class that holds a SQL database configuration. 

This configuration is parsed into a database URI and
used in either the `SQLALCHEMY_DATABASE_URI` or `SQLALCHEMY_BINDS` configuration variables.