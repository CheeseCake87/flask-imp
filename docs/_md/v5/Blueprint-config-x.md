```
Menu = Blueprint/config.x
Title = The Flask-Imp Blueprint Config File
```

---

**Recommendation:** Try and favour the use of a py file for your
configuration settings, as this will trigger reloads under
debug mode.

Also, the bonus of being able to use Python to programmatically
set values is nice.

---

The Flask-Imp Blueprint loads configuration settings from either a class
defined in a module or from a toml file.

This file needs to sit next to the `__init__.py` file.

```python
from flask_imp import Blueprint

bp = Blueprint(__name__)  # will look for config.toml / config.py w/ Config class
# or
bp = Blueprint(__name__, config="config.Development")  # will look for Development class in config.py
# or
bp = Blueprint(__name__, config="development.toml")  # will look for development.toml file
```

For more information about the `config` parameter see: [Imp / config.x](Imp-config-x.html)

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

```python
from flask_imp import ImpBlueprintConfig, DatabaseConfig


class Config(ImpBlueprintConfig):
    ENABLED: bool = True
    URL_PREFIX: str = "/"
    # SUBDOMAIN: str = ""
    # URL_DEFAULTS: dict = {}
    STATIC_FOLDER: str = "static"
    TEMPLATE_FOLDER: str = "templates"
    STATIC_URL_PATH: str = "/static"
    # ROOT_PATH: str = ""
    # CLI_GROUP: str = ""

    INIT_SESSION: dict = {
        "www_session": "yes"
    }

    DATABASE_BINDS: set[DatabaseConfig] = {
        DatabaseConfig(
            ENABLED=True,
            DIALECT="sqlite",
            NAME="www",
            BIND_KEY="www",
            LOCATION="",
            PORT=0,
            USERNAME="",
            PASSWORD="",
        )
    }
```

### Example `config.toml` configuration file:

```toml
ENABLED = "yes"

[SETTINGS]
URL_PREFIX = "/"
#SUBDOMAIN = ""
#URL_DEFAULTS = {}
STATIC_FOLDER = "static"
TEMPLATE_FOLDER = "templates"
STATIC_URL_PATH = "/static"
#ROOT_PATH = ""
#CLI_GROUP = ""

[SESSION]
www_session = "yes"

# Set ENABLED to true to allow the blueprint
# to create a database bind, change settings accordingly.
[DATABASE_BIND]
ENABLED = true
DIALECT = "sqlite"
DATABASE_NAME = "www"
BIND_KEY = "www"
LOCATION = ""
PORT = ""
USERNAME = ""
PASSWORD = ""
```

These config files reflect the args that are passed to a regular Flask Blueprint class,
with the addition of the ability to enable/disable the Blueprint, set session variables and
include database binds.

For more information about the args of a regular Flask Blueprint see:
[Flask docs (Blueprint)](https://flask.palletsprojects.com/en/3.0.x/api/#flask.Blueprint)

### Session Variables

You can set the default session variables for the blueprint by setting values in `INIT_SESSION`, these can be loaded
using the before_request function in the blueprint.

```python
@blueprint.before_app_request
def load_session():
    blueprint._init_session()
```

### Database Binds

You can also allow the blueprint to create a database bind, by setting `ENABLED` to `true` in the `DATABASE_BIND`
section of the toml file, or by adding to the `DATABASE_BINDS` set of the `Config` class.

**Using a py config file will allow you to set multiple database binds for the blueprint.**

This will add to the Flask app's `SQLALCHEMY_BINDS` config variable, and allows blueprints to be more modular
with their database connections.

Including the attribute `__bind_key__` in the blueprint's model(s) will match the model to the database bind.

```python
class User(db.Model):
    __bind_key__ = "example"
    ...
```
