```
Menu = Blueprint.x/import_models
Title = Blueprint.import_models
```

```python
import_models(folder: str = "models") -> None
```

---

Will import all the models from the given folder relative to the Blueprint's root directory.

Works the same as [Imp.x / import_models](imp_x-import_models.html) but relative to the Blueprint root.

Blueprint models will also be available in the [Imp.x / model](imp_x-model.html) lookup.

```text
my_blueprint/
├── routes/...
├── static/...
├── templates/...
│
├── animal_models.py
│
├── __init__.py
└── config.toml
```

**or**

```text
my_blueprint/
├── routes/...
├── static/...
├── templates/...
│
├── models/
│   └── animals.py
│
├── __init__.py
└── config.toml
```

File: `my_blueprint/__init__.py`

```python
from flask_imp import Blueprint

bp = Blueprint(__name__)

bp.import_resources("routes")
bp.import_models("animal_models.py")
```

**or**

```python
from flask_imp import Blueprint

bp = Blueprint(__name__)

bp.import_resources("routes")
bp.import_models("models")
```

File: `my_blueprint/animal_models.py` or `my_blueprint/models/animals.py`

```python
from app import db


class Animals(db.Model):
    animal_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    species = db.Column(db.String(64), index=True, unique=True)
```



