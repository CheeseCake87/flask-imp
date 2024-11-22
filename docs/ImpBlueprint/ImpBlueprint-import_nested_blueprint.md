# ImpBlueprint.import_nested_blueprint

```python
import_nested_blueprint(self, blueprint: str) -> None
```

---

Import a specified Flask-Imp or standard Flask Blueprint relative to the Blueprint root.

Works the same as [Imp / import_blueprint](imp-import_blueprint.md) but relative to the Blueprint root.

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
│
├── __init__.py
```

File: `my_blueprint/__init__.py`

```python
from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig

bp = ImpBlueprint(__name__, ImpBlueprintConfig(
    enabled=True,
    static_folder="static",
    template_folder="templates",
))

bp.import_resources("routes")
bp.import_nested_blueprint("my_nested_blueprint")
```

File: `my_blueprint/my_nested_blueprint/__init__.py`

```python
from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig

bp = ImpBlueprint(__name__, ImpBlueprintConfig(
    enabled=True,
    static_folder="static",
    template_folder="templates",
))

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
