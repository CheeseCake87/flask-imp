```
Menu = ImpBlueprint.x/import_nested_blueprints
Title = ImpBlueprint.import_nested_blueprints
```

```python
import_nested_blueprints(self, folder: str) -> None
```

---

Will import all the Blueprints from the given folder relative to the Blueprint's root directory.

Uses [Blueprint.x / import_nested_blueprint](blueprint_x-import_nested_blueprint.html) to import blueprints from
the specified folder.

Blueprints that are imported this way will be scoped to the parent Blueprint that imported them.

`url_for('my_blueprint.nested_bp_one.index')`

`url_for('my_blueprint.nested_bp_two.index')`

`url_for('my_blueprint.nested_bp_three.index')`

```text
my_blueprint/
├── routes/...
├── static/...
├── templates/...
│
├── nested_blueprints/
│   │
│   ├── nested_bp_one/
│   │   ├── ...
│   │   ├── __init__.py
│   ├── nested_bp_two/
│   │   ├── ...
│   │   ├── __init__.py
│   └── nested_bp_three/
│       ├── ...
│       ├── __init__.py
│
├── __init__.py
```

File: `my_blueprint/__init__.py`

```python
from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig

bp = ImpBlueprint(__name__, ImpBlueprintConfig(
    enabled=True,
))

bp.import_resources("routes")
bp.import_nested_blueprints("nested_blueprints")
```