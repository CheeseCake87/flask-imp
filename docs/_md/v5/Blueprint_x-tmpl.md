```
Menu = Blueprint.x/tmpl
Title = Blueprint.tmpl
```

```python
tmpl(template: str) -> str
```

---

Scopes the template lookup to the name of the blueprint (this takes from the `__name__` attribute of the Blueprint).

Due to the way Flask templating works, and to avoid template name collisions.
It is standard practice to place the name of the Blueprint in the template path,
then to place any templates under that folder.

```text
my_blueprint/
├── routes/
│   └── index.py
├── static/...
│
├── templates/
│   └── my_blueprint/
│       └── index.html
│
├── __init__.py
└── config.toml
```

File: `my_blueprint/routes/index.py`

```python
from flask import render_template

from .. import bp


@bp.route("/")
def index():
    return render_template(bp.tmpl("index.html"))
```

`bp.tmpl("index.html")` will output `"my_blueprint/index.html"`.
