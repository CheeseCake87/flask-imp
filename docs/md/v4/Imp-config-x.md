```
Menu = Imp/config.x
Title = The Flask-Imp Config File
```

---

**Recommendation:** Try and favour the use of a py file for your
configuration settings, as this will trigger reloads under
debug mode.

Also, the bonus of being able to use Python to programmatically
set values is nice.

---

Flask-Imp loads configuration settings from either a class
defined in a module or from a toml file.

**This example:**

```python

def create_app():
    app = Flask(__name__)
    imp.init_app(app, config="dev.config.toml")

```

Will load configuration from the `dev.config.toml` file.

**This example:**

```python

def create_app():
    app = Flask(__name__)
    imp.init_app(app, config="config.Config")

```

Will load the configuration from the `Config` class from the `config.py` file.

Both of these files need to be located in the root of the app.

The config class must be an instance of `ImpConfig` from `flask_imp`.

You can also set the config by using the `IMP_CONFIG` environment
variable, but you will need to omit or set the `config` parameter to `None`.

For example, given the following folder structure:

```text
Project/
├── app/
│   ├── ...
│   ├── __init__.py
│   ├── config.py
│   └── dev.config.toml
├── venv/...
└── ...
```

You'd set the `IMP_CONFIG=dev.config.toml` and this will load the `dev.config.toml` file.

### Using environment variables

#### toml

In a toml config, you can set environment variables by using `{{ }}`

```toml
TEST_VALUE = "{{ test_value }}"
```

You can also set the type of the variable by using `:type` after the variable name.

```toml
TEST_VALUE = "{{ test_value:int }}"
```

**Supported types are `int`, `float`, `bool`, `str`.**

#### py

In a py config, you can set environment variables by using `os.getenv`.

```python
TEST_VALUE = os.getenv("TEST_VALUE", "default_value_here")
```

### Example `config.py` configuration file:

```text
Project/
├── app/
│   ├── ...
│   ├── __init__.py
│   └── config.py
├── venv/...
└── ...
```

```python
from flask_imp import (
    FlaskConfig,
    ImpConfig,
    DatabaseConfig
)


class Config(ImpConfig):
    FLASK = FlaskConfig(
        # DEBUG=False,
        # PROPAGATE_EXCEPTIONS = True,
        TRAP_HTTP_EXCEPTIONS=False,
        # TRAP_BAD_REQUEST_ERRORS = True,
        SECRET_KEY="flask-imp",  # CHANGE ME
        SESSION_COOKIE_NAME="session",
        # SESSION_COOKIE_DOMAIN = "domain-here.com",
        # SESSION_COOKIE_PATH = "/",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_SAMESITE="Lax",
        PERMANENT_SESSION_LIFETIME=3600,  # 1 hour,
        SESSION_REFRESH_EACH_REQUEST=True,
        USE_X_SENDFILE=False,
        # SEND_FILE_MAX_AGE_DEFAULT = 43200,
        ERROR_404_HELP=True,
        # SERVER_NAME = "localhost:5000",
        APPLICATION_ROOT="/",
        PREFERRED_URL_SCHEME="http",
        # MAX_CONTENT_LENGTH = 0,
        # TEMPLATES_AUTO_RELOAD = True,
        EXPLAIN_TEMPLATE_LOADING=False,
        MAX_COOKIE_SIZE=4093,
    )

    # This will set the default session variables for the app.
    INIT_SESSION = {
        "logged_in": False,
    }

    # Below are extra settings that Flask-Imp uses but relates to Flask-SQLAlchemy.
    # This sets the file extension for SQLite databases, and where to create the folder
    # that the database will be stored in.
    # True will create the folder on the same level as your
    # app, False will create the folder in the app root.
    SQLITE_DB_EXTENSION = ".sqlite"
    SQLITE_STORE_IN_PARENT = False
    #

    # SQLAlchemy settings that will be passed to Flask
    # Any SQLAlchemy setting here will overwrite anything
    # set in the config above
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False
    #

    # Main database settings, this will be converted to SQLALCHEMY_DATABASE_URI
    DATABASE_MAIN = DatabaseConfig(
        ENABLED=True,
        DIALECT="sqlite",
        NAME="main",
        LOCATION="",
        PORT=0,
        USERNAME="",
        PASSWORD="",
    )

    # Binds are additional databases that can be used in your app
    # These will be added to the SQLALCHEMY_BINDS dictionary
    # DATABASE_BINDS = {
    #     DatabaseConfig(
    #         ENABLED=True,
    #         DIALECT="sqlite",
    #         NAME="additional_database",
    #         BIND_KEY="additional_database",
    #         LOCATION="",
    #         PORT=0,
    #         USERNAME="",
    #         PASSWORD="",
    #     )
    # }
```

### Example `config.toml` configuration file:

```text
Project/
├── app/
│   ├── ...
│   ├── __init__.py
│   └── config.toml
├── venv/...
└── ...
```

```toml
# Flask-Imp Config File
# ------------------------
# Updates the Flask app config with the variables below.
# If any variable below does not exist in the standard Flask env
# vars it is created and will be accessible using
# app.config. All key names defined below will be
# capitalised when imported.
[FLASK]
#DEBUG = false
#PROPAGATE_EXCEPTIONS = true
TRAP_HTTP_EXCEPTIONS = false
#TRAP_BAD_REQUEST_ERRORS = true
SECRET_KEY = "super_secret_key"
SESSION_COOKIE_NAME = "session"
#SESSION_COOKIE_DOMAIN = "domain-here.com"
#SESSION_COOKIE_PATH = "/"
SESSION_COOKIE_HTTPONLY = true
SESSION_COOKIE_SECURE = false
SESSION_COOKIE_SAMESITE = "Lax"
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
SESSION_REFRESH_EACH_REQUEST = true
USE_X_SENDFILE = false
#SEND_FILE_MAX_AGE_DEFAULT = 43200
ERROR_404_HELP = true
#SERVER_NAME = "localhost:5000"
APPLICATION_ROOT = "/"
PREFERRED_URL_SCHEME = "http"
#MAX_CONTENT_LENGTH = 0
#TEMPLATES_AUTO_RELOAD = true
EXPLAIN_TEMPLATE_LOADING = false
MAX_COOKIE_SIZE = 4093


# This will set the default session variables for the app.
# Anything here will be accessible using session["your_var_name"]
# or session.get("your_var_name")
[SESSION]
logged_in = false

# These settings are spcific to the Flask-SQLAlchemy extension.
# Anything here will be accessible using app.config
[SQLALCHEMY]
SQLALCHEMY_ECHO = false
SQLALCHEMY_TRACK_MODIFICATIONS = false
SQLALCHEMY_RECORD_QUERIES = false
# Below are extra settings that Flask-Imp uses but relates to Flask-SQLAlchemy.
# This sets the file extension for SQLite databases, and where to create the folder
# that the database will be stored in. true will create the folder on the same level as your
# app, false will create the folder in the app root.
SQLITE_DB_EXTENSION = ".sqlite"
SQLITE_STORE_IN_PARENT = true

# [DATABASE.MAIN] is loaded as SQLALCHEMY_DATABASE_URI
# Dialets = mysql / postgresql / sqlite / oracle / mssql

# Uncomment below to generate the SQLALCHEMY_DATABASE_URI.
[DATABASE.MAIN]
ENABLED = true
DIALECT = "sqlite"
NAME = "database"
LOCATION = "db"
PORT = ""
USERNAME = ""
PASSWORD = ""

# Adding another database is as simple as adding a new section.
# [DATABASE.ANOTHER] will then be accessible using SQLALCHEMY_BINDS
# The bind key will be stored as a lowercase value, so "ANOTHER" will
# be accessible as "another"
# You can then use the bind key in the model as follows:
# class MyModel(db.Model):
#     __bind_key__ = "another"
#     ...

# Uncomment below to generate and add to SQLALCHEMY_BINDS.
#[DATABASE.ANOTHER]
#ENABLED = true
#DIALECT = "sqlite"
#NAME = "database_another"
#LOCATION = "db"
#PORT = ""
#USERNAME = "user"
#PASSWORD = "password"

```
