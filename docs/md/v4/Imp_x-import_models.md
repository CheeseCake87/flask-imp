```
Menu = Imp.x/import_models
Title = Imp.import_models
```

```python
import_models(file_or_folder: str) -> None
```

---

Imports all the models from the given file or folder relative to the Flask app root.

Each Model that is imported will be available in the `imp.model` lookup method.
See [Imp.x / model](imp_x-model.html) for more information.

##### Example of importing models from a file

```text
app
├── my_blueprint
│   ├── ...
│   └── __init__.py
├── users_model.py
├── ...
└── __init__.py
```

File: `app/__init__.py`

```python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_imp import Imp

db = SQLAlchemy()
imp = Imp()


def create_app():
    app = Flask(__name__)
    imp.init_app(app)
    db.init_app(app)  # must be below imp.init_app

    imp.import_blueprint("my_blueprint")
    imp.import_models("users_model.py")

    return app
```

File: `app/users_model.py`

```python
from app import db


class User(db.Model):
    attribute = db.Column(db.String(255))
```

##### Example of importing models from a folder

```text
app
├── my_blueprint
│   ├── ...
│   └── __init__.py
├── models/
│   ├── boats.py
│   ├── cars.py
│   └── users.py
├── ...
└── __init__.py
```

```python
def create_app():
    ...
    imp.import_models("models")
    ...
```
