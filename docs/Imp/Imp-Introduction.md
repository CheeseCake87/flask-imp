# Flask-Imp Introduction

Flask-Imp is a Flask extension that provides auto import methods for various Flask resources. It will import models,
blueprints, and other resources. It uses the importlib module to achieve this.

Flask-Imp favors the application factory pattern as a project structure, and is opinionated towards using
Blueprints. However, you can use Flask-Imp without using Blueprints.

Here's an example of a standard Flask-Imp project structure:

```text
app/
├── blueprints/
│   ├── admin/...
│   ├── api/...
│   └── www/...
├── resources/
│   ├── filters/...
│   ├── context_processors/...
│   ├── static/...
│   └── templates/...
├── models/...
└── __init__.py
```

Here's an example of the `app/__init__.py` file:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_imp import Imp
from flask_imp.config import FlaskConfig, ImpConfig

db = SQLAlchemy()
imp = Imp()


def create_app():
    app = Flask(__name__)
    FlaskConfig(
        secret_key="super_secret_key",
        app_instance=app,
    )

    imp.init_app(app, config=ImpConfig(
        init_session={"logged_in": False},
    ))
    imp.import_app_resources("resources")
    imp.import_models("models")
    imp.import_blueprints("blueprints")

    db.init_app(app)

    return app
```

The Flask configuration can be loaded from any standard Flask configuration method, or from the `FlaskConfig` class
shown above.

This class contains the standard Flask configuration options found in the Flask documentation.

The `ImpConfig` class is used to configure the `Imp` instance.

The `init_session` option of the `ImpConfig` class is used to set the initial session variables for the Flask app.
This happens before the request is processed.

`ImpConfig` also has the ability to set `SQLALCHEMY_DATABASE_URI` and `SQLALCHEMY_BINDS`

For more information about the configuration setting see
[flask_imp_config-impconfig.md](flask_imp_config-impconfig.md).

`import_app_resources` will walk one level deep into the `resources` folder, and import
all `.py` files as modules.
It will also check for the existence of a `static` and `templates` folder, and register them with the Flask app.

There is a couple of options for `import_app_resources` to control what
is imported, see: [Imp / import_app_resources](imp-import_app_resources.md)

`import_models` will import all Model classes from the specified file or folder. It will also place each model found
into a lookup table that you can access via `imp.model`

See more about how import_models and the lookup
here: [Imp / import_models](imp-import_models.md) and [Imp / model](imp-model.md)

`import_blueprints` expects a folder that contains many Blueprint as Python packages.
It will check each blueprint folder's `__init__.py` file for an instance of a Flask Blueprint or a
Flask-Imp Blueprint. That instant will then be registered with the Flask app.

See more about how importing blueprints work here: [ImpBlueprint / Introduction](impblueprint-introduction.md)
