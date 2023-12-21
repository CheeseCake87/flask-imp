# Welcome to the Flask-Imp Documentation

## What is Flask-Imp?

Flask-Imp's main purpose is to help simplify the importing of blueprints, resources, and models. It has a few extra
features built in to help with securing pages and password authentication.

## Install Flask-Imp

```bash
pip install flask-imp
```

## Getting Started

To get started right away, you can utilize the CLI commands to create a new Flask-Imp project.

```bash
flask-imp init
```

### Minimal Flask-Imp Setup

Run the following command to create a minimal Flask-Imp project.

```bash
flask-imp init -n app --minimal
```

See [CLI Commands / flask-imp init](cli_commands-flask-imp_init.html) for more information.

### Build minimal manually

#### Folder Structure

```text
app/
├── resources/
│   ├── static/...
│   ├── templates/
│   │   └── index.html
│   └── index.py
├── default.config.toml
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

We recommend using a virtual environment, then installing Flask-Imp.

**Linux / MacOS**

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

