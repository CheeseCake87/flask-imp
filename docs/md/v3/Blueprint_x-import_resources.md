```
Menu = Blueprint.x/import_resources
Title = Blueprint.import_resources
```

```python
import_resources(folder: str = "routes") -> None
```

---

Will import all the resources (cli, routes, filters, context_processors...) from the given folder relative to the
Blueprint's root directory.

```text
my_blueprint
├── user_routes
│   ├── user_dashboard.py
│   └── user_settings.py
├── car_routes
│   ├── car_dashboard.py
│   └── car_settings.py
├── static/...
├── templates/
│   └── my_blueprint/
│       ├── user_dashboard.html
│       └── ...
├── __init__.py
└── config.toml
```

File: `my_blueprint/__init__.py`

```python
from flask_imp import Blueprint

bp = Blueprint(__name__)

bp.import_resources("user_routes")
bp.import_resources("car_routes")
```

File: `my_blueprint/user_routes/user_dashboard.py`

```python
from flask import render_template

from .. import bp

@bp.route("/user-dashboard")
def user_dashboard():
    return render_template(bp.tmpl("user_dashboard.html"))
```
