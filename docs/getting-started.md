# Getting Started

## Install Flask-Imp

**Install in a [Virtual environment](#setup-a-virtual-environment)**

```bash
pip install flask-imp
```

To get started right away, you can use the CLI commands to create a new Flask-Imp project.

```bash
flask-imp init
```

### Minimal Flask-Imp Setup

Run the following command to create a minimal Flask-Imp project.

```bash
flask-imp init -n app --minimal
```

### The minimal structure

#### Folder Structure

```text
app/
├── resources/
│   ├── static/...
│   ├── templates/
│   │   └── index.html
│   └── index.py
└── __init__.py
```

File: `app/__init__.py`

```python
from flask import Flask

from flask_imp import Imp
from flask_imp.config import FlaskConfig, ImpConfig

imp = Imp()


def create_app():
    app = Flask(__name__, static_url_path="/")
    FlaskConfig(
        secret_key="secret_key",
        app_instance=app
    )

    imp.init_app(app, ImpConfig())

    imp.import_resources()
    # Takes argument 'folder' default folder is 'resources'

    return app
```

File: `app/resources/routes.py`

```python
from flask import Flask
from flask import render_template

def include(app: Flask):
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

**For more examples see: [CLI Commands / flask-imp init](CLI_Commands/CLI_Commands-flask-imp_init.md)**

---

## Securing Routes

Use the `checkpoint` decorator to secure routes, here's an example:

Update the `app/resources/routes.py` file with the following code:

```python
from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import session
from flask_imp.security import checkpoint, SessionCheckpoint
from flask_imp.utilities import lazy_url_for

LOGIN_REQUIRED = SessionCheckpoint(
    session_key="logged_in",
    values_allowed=True,
).action(
    fail_url=lazy_url_for("login_required")
)


def include(app: Flask):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/protected")
    @checkpoint(LOGIN_REQUIRED)
    def protected():
        return "You are logged in!"

    @app.route("/login-required")
    def login_required():
        return "You need to login first!"

    @app.route("/login")
    def login():
        session["logged_in"] = True
        return redirect(url_for("protected"))

    @app.route("/logout")
    def logout():
        session["logged_in"] = False
        return redirect(url_for("index"))
```

**See more at: [Security / checkpoint](Security/flask_imp_security-checkpoint.md)**

## Setup a Virtual Environment

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
