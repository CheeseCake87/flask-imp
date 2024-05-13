# Welcome to the Flask-Imp Documentation

## What is Flask-Imp?

Flask-Imp's main purpose is to help simplify the importing of blueprints, resources, and models. It has a few extra
features built in to help with securing pages and password authentication.

## Install Flask-Imp

```bash
pip install flask-imp
```

## Getting Started

To get started right away, you can use the CLI commands to create a new Flask-Imp project.

```bash
flask-imp init
```

### Minimal Flask-Imp Setup

Run the following command to create a minimal Flask-Imp project.

```bash
flask-imp init -n app --minimal --pyconfig
```

See [CLI Commands / flask-imp init](cli_commands-flask-imp_init.html) for more information.

### The minimal structure

#### Folder Structure

```text
app/
├── resources/
│   ├── static/...
│   ├── templates/
│   │   └── index.html
│   └── index.py
├── config.py
└── __init__.py
```

File: `app/__init__.py`

```python
from flask import Flask

from flask_imp import Imp

imp = Imp()


def create_app():
    app = Flask(__name__)
    imp.init_app(app)

    imp.import_app_resources()
    # Takes argument 'folder' default folder is 'resources'

    return app
```

File: `app/config.py`

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
        SECRET_KEY="flask-imp",
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

    # INIT_SESSION = {
    #     "logged_in": False,
    # }

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

    # Main database settings, this will be turned int the SQLALCHEMY_DATABASE_URI
    # DATABASE_MAIN = DatabaseConfig(
    #     ENABLED=True,
    #     DIALECT="sqlite",
    #     NAME="main",
    #     LOCATION="",
    #     PORT=0,
    #     USERNAME="",
    #     PASSWORD="",
    # )

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

File: `app/resources/index.py`

```python
from flask import current_app as app
from flask import render_template


@app.route("/")
def index():
    return render_template("index.html")
```

File: `app/resources/templates/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask-Imp</title>
</head>
<body>
<h1>Flask-Imp</h1>
</body>
</html>
```

---

Setting up a virtual environment is recommended.

**Linux / Darwin**

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
```

```text
.\venv\Scripts\activate
```