```
Menu = Blueprint/config.toml
Title = The Flask-Imp Blueprint Config File
```

The Flask-Imp Blueprint will load configuration from a `config.toml` file, which is located in the same directory as the
`__init__.py` file.

File: `config.toml`

```toml
enabled = "yes"

[settings]
url_prefix = ""
subdomain = ""
url_defaults = { }
static_folder = ""
template_folder = ""
static_url_path = ""
#root_path = ""
#cli_group = ""

[session]
var = ""

# Set ENABLED to true to allow the blueprint
# to create a database bind, change settings accordingly.
[DATABASE_BIND]
ENABLED = true
DIALECT = "sqlite"
DATABASE_NAME = "example"
LOCATION = ""
PORT = ""
USERNAME = ""
PASSWORD = ""
```

This config reflects the args that are passed to a regular Flask Blueprint class, the addition of the ability to
enable/disable the Blueprint, and set session variables.

For more information about the args of a regular Flask Blueprint see:
[Flask docs (Blueprint)](https://flask.palletsprojects.com/en/3.0.x/api/#flask.Blueprint)

You can also allow the blueprint to create a database bind, by setting `ENABLED` to `true` in the `DATABASE_BIND`
section.

This will add to the Flask app's `SQLALCHEMY_BINDS` config variable, and allows blueprints to be more modular
with their database connections.

Including the attribute `__bind_key__` in the blueprint's model(s) will match the model to the database bind.

```python
class User(db.Model):
    __bind_key__ = "example"
    ...
```

##### Example of advance use case for blueprint config files:

```text
testing_blueprint/
├── routes/
│   └── index.py
├── static/
│   └── ...
├── templates/
│   └── www/
│       └── index.html
├── __init__.py
├── pro_config.py
└── dev_config.toml
```

```python
from app import app
from flask_imp import Blueprint

bp = Blueprint(
    __name__,
    config_file="dev_config.toml" if app.config["DEBUG"] else "pro_config.py"
)

bp.import_resources("routes")


@bp.before_app_request
def before_app_request():
    bp.init_session()
```

File: `pro_config.py`

```toml
enabled = "no"

[settings]
#url_prefix = ""
#subdomain = ""
#url_defaults = { }
#static_folder = ""
#template_folder = ""
#static_url_path = ""
#root_path = ""
#cli_group = ""

[session]
#var = ""

# Set ENABLED to true to allow the blueprint
# to create a database bind, change settings accordingly.
[DATABASE_BIND]
ENABLED = false
DIALECT = "sqlite"
DATABASE_NAME = "example"
LOCATION = ""
PORT = ""
USERNAME = ""
PASSWORD = ""
```

File: `dev_config.py`

```toml
enabled = "yes"

[settings]
url_prefix = "/testing"
#subdomain = ""
#url_defaults = { }
static_folder = "static"
template_folder = "templates"
#static_url_path = ""
#root_path = ""
#cli_group = ""

[session]
#var = ""

# Set ENABLED to true to allow the blueprint
# to create a database bind, change settings accordingly.
[DATABASE_BIND]
ENABLED = true
DIALECT = "sqlite"
DATABASE_NAME = "example"
LOCATION = ""
PORT = ""
USERNAME = ""
PASSWORD = ""
```

In the example above, the `testing_blueprint` will only be enabled if the Flask app is running in debug mode.