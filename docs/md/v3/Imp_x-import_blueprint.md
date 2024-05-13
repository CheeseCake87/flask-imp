```
Menu = Imp.x/import_blueprint
Title = Imp.import_blueprint
```

```python
import_blueprint(self, blueprint: str) -> None
```

---

Import a specified Flask-Imp or standard Flask Blueprint relative to the Flask app root.


```text
app
├── my_blueprint
│   ├── ...
│   └── __init__.py
├── ...
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

    imp.import_blueprint("my_blueprint")

    return app
```

Flask-Imp Blueprints have the ability to import configuration from a toml file, import resources, and initialize session
variables.

For more information on how Flask-Imp Blueprints work, see the [Blueprint / Introduction](blueprint-introduction.html)

##### Example of 'my_blueprint' as a Flask-Imp Blueprint:

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

File: `routes / index.py`

```python
from .. import bp


@bp.route("/")
def index():
    return "regular_blueprint"
```

##### Example of 'my_blueprint' as a standard Flask Blueprint:

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

Both of the above examples will work with `imp.import_blueprint("my_blueprint")`, they will be registered
with the Flask app, and will be accessible via `url_for("my_blueprint.index")`.