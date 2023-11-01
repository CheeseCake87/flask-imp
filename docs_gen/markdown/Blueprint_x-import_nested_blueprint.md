```
Menu = Blueprint.x/import_nested_blueprint
Title = Blueprint.import_nested_blueprint
```

```python
import_nested_blueprint(self, blueprint: str) -> None
```

---

Import a specified Flask-Imp or standard Flask Blueprint relative to the Blueprint root.

Works the same as [Imp.x / import_blueprint](imp_x-import_blueprint.html) but relative to the Blueprint root.

Blueprints that are imported this way will be scoped to the parent Blueprint that imported them.

`url_for('my_blueprint.my_nested_blueprint.index')`

```text
my_blueprint/
├── routes/...
├── static/...
├── templates/...
│
├── my_nested_blueprint/
│   ├── routes/
│   │   └── index.py
│   ├── static/...
│   ├── templates/...
│   ├── __init__.py
│   └── config.toml
│
├── __init__.py
└── config.toml
```

File: `my_blueprint/__init__.py`

```python
from flask_imp import Blueprint

bp = Blueprint(__name__)

bp.import_resources("routes")
bp.import_nested_blueprint("my_nested_blueprint")
```

File: `my_blueprint/my_nested_blueprint/__init__.py`

```python
from flask_imp import Blueprint

bp = Blueprint(__name__)

bp.import_resources("routes")
```

File: `my_blueprint/my_nested_blueprint/routes/index.py`

```python
from flask import render_template

from .. import bp


@bp.route("/")
def index():
    return render_template(bp.tmpl("index.html"))
```