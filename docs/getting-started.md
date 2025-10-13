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

See [CLI Commands / flask-imp init](CLI_Commands/CLI_Commands-flask-imp_init.md) for more information.

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

---

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
