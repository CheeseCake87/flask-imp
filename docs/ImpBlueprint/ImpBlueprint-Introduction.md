# Flask-Imp Blueprint Introduction

The Flask-Imp Blueprint inherits from the Flask Blueprint class, then adds some additional methods to allow for auto
importing of models, resources and other nested blueprints.

The Flask-Imp Blueprint requires you to provide the `ImpBlueprintConfig` class as the second argument to the Blueprint.

Here's an example of a Flask-Imp Blueprint structure:

```text
www/
├── nested_blueprints/
│   ├── blueprint_one/
│   │   ├── ...
│   │   └── __init__.py
│   └── blueprint_two/
│       ├── ...
│       └── __init__.py
├── standalone_nested_blueprint/
│   ├── ...
│   └── __init__.py
├── models/
│   └── ...
├── routes/
│   └── index.py
├── static/
│   └── ...
├── templates/
│   └── www/
│       └── index.html
└── __init__.py
```

File: `__init__.py`

```python
from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig

bp = ImpBlueprint(__name__, ImpBlueprintConfig(
    enabled=True,
    url_prefix="/www",
    static_folder="static",
    template_folder="templates",
    init_session={"logged_in": False},
))

bp.import_resources("routes")
bp.import_models("models")
bp.import_nested_blueprints("nested_blueprints")
bp.import_nested_blueprint("standalone_nested_blueprint")
```

The `ImpBlueprintConfig` class is used to configure the Blueprint. It provides a little more flexibility than the
standard Flask Blueprint configuration, like the ability to enable or disable the Blueprint.

`ImpBlueprintConfig`'s `init_session` works the same as `ImpConfig`'s `init_session`, this will add the session data to
the Flask app's session object on initialization of the Flask app.

To see more about configuration see: [flask_imp.config / ImpBlueprintConfig](../Config/flask_imp_config-impblueprintconfig.md)

`import_resources` method will walk one level deep into the `routes` folder, and import all `.py` files as modules.
For more information see: [ImpBlueprint / import_resources](../ImpBlueprint/ImpBlueprint-import_resources.md)

`import_models` works the same as `imp.import_models`, it will look for instances of `db.Model` and import them. These
will also be available in the model lookup method `imp.model`.
For more information see: [Imp / import_models](../Imp/Imp-import_models.md)

`import_nested_blueprints` will do the same as `imp.import_blueprints`, but will register the blueprints found as
nested to the current blueprint. For example `www.blueprint_one.index`

`import_nested_blueprint` behaves the same as `import_nested_blueprints`, but will only import a single blueprint.

