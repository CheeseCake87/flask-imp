# Imp.import_blueprints

```python
import_blueprints(self, folder: str) -> None
```

---

Import all Flask-Imp or standard Flask Blueprints from a specified folder relative to the Flask app root.

```text
app/
├── blueprints/
│   ├── admin/
│   │   ├── ...
│   │   └── __init__.py
│   ├── www/
│   │   ├── ...
│   │   └── __init__.py
│   └── api/
│       ├── ...
│       └── __init__.py
├── ...
└── __init__.py
```

File: `app/__init__.py`

```python
from flask import Flask

from flask_imp import Imp

imp = Imp()


def create_app():
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates"
    )
    imp.init_app(app)

    imp.import_blueprints("blueprints")

    return app
```

This will import all Blueprints from the `blueprints` folder using the `Imp.import_blueprint` method.
See [Imp / import_blueprint](../Imp/Imp-import_blueprint.md) for more information.

