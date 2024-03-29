```
Menu = Imp/x.config.toml
Title = The Flask-Imp Config File
```

Flask-Imp loads configuration settings from a toml file found in the root of your app package.

`app/default.config.toml` is the default config file, this will be created if no config file is found or set.

Here's an example file structure:

```text
Project/
├── app/
│   ├── ...
│   ├── __init__.py
│   └── default.config.toml
├── venv/...
└── ...
```

Here's an example of the default config file that is created:

```toml
# Flask-Imp Config File
# ------------------------
# Updates the Flask app config with the variables below.
# If any variable below does not exist in the standard Flask env
# vars it is created and will be accessible using
# app.config. All key names defined below will be
# capitalised when imported.
[FLASK]
DEBUG = false
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
#[DATABASE.MAIN]
#ENABLED = true
#DIALECT = "sqlite"
#DATABASE_NAME = "database"
#LOCATION = "db"
#PORT = ""
#USERNAME = "database"
#PASSWORD = "password"

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
#DATABASE_NAME = "database_another"
#LOCATION = "db"
#PORT = ""
#USERNAME = "user"
#PASSWORD = "password"

```

To change what config file is loaded, you can set the `IMP_CONFIG` environment
variable to the name of the config file you want to load.

For example, given the following folder structure:

```text
Project/
├── app/
│   ├── ...
│   ├── __init__.py
│   ├── production.config.toml
│   └── default.config.toml
├── venv/...
└── ...
```

You'd set the `IMP_CONFIG=production.config.toml`

Or you can set the file in the `imp.init_app()` method:

```python

def create_app():
    app = Flask(__name__)
    imp.init_app(app, app_config_file="production.config.toml")

```