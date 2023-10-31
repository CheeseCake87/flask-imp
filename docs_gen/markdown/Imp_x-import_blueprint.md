```
Menu = Imp.x/import_blueprint
Title = Imp.import_blueprint
```

```python
import_blueprint(self, blueprint: str) -> None
```

---

Import a specified Flask-Imp or standard Flask Blueprint.

```python
from flask import Flask

from flask_imp import Imp

imp = Imp()


def create_app():
    app = Flask(__name__)
    imp.init_app(app)

    imp.import_blueprint("my_blueprint")

    return app
```

Flask-Imp Blueprints have the ability to import configuration from a toml file, import resources, and initialize session
variables.

#### Example of a Flask-Imp Blueprint:

```text
app
├── my_blueprint
│   ├── routes
│   │   └── index.py
│   ├── static
│   │   └── css
│   │       └── style.css
│   ├── templates
│   │   └── my_blueprint
│   │       └── index.html
│   ├── __init__.py
│   └── config.toml
└── ...
```

File: `__init__.py`

```python
from flask_imp import Blueprint

bp = Blueprint(__name__)

bp.import_resources("routes")


@bp.before_app_request
def before_app_request():
    bp.init_session()
```

#### Example of a standard Flask Blueprint:

```text
app
├── my_blueprint
│   ├── ...
│   └── __init__.py
└── ...
```

File: `__init__.py`

```python
from flask import Blueprint

bp = Blueprint("my_blueprint", __name__, url_prefix="/my-blueprint")


@bp.route("/")
def index():
    return "regular_blueprint"
```