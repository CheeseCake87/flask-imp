# Imp.register_imp_blueprint

```python
register_imp_blueprint(self, imp_blueprint: ImpBlueprint) -> None
```

---

Manually register a ImpBlueprint.

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

DO_IMPORT = True


def create_app():
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates"
    )
    imp.init_app(app)

    if DO_IMPORT:
        from app.my_blueprint import bp

        imp.register_imp_blueprint(bp)

    return app
```
