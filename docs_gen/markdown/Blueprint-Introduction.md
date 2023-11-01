```
Menu = Blueprint/Introduction
Title = Flask-Imp Blueprint Introduction
```

The Flask-Imp Blueprint inherits from the Flask Blueprint class, then adds some additional methods to allow for auto
importing of models, resources and other nested blueprints.

The Flask-Imp Blueprint reads configuration from a config.toml file, which is located in the same directory as the
`__init__.py` file.

Here's an example of a Flask-Imp Blueprint structure:

```text
www/
├── nested_blueprints/
│   ├── blueprint_one/
│   │   ├── ...
│   │   ├── __init__.py
│   │   └── config.toml
│   └── blueprint_two/
│       ├── ...
│       ├── __init__.py
│       └── config.toml
├── standalone_nested_blueprint/
│   ├── ...
│   ├── __init__.py
│   └── config.toml
├── models/
│   └── ...
├── routes/
│   └── index.py
├── static/
│   └── ...
├── templates/
│   └── www/
│       └── index.html
├── __init__.py
└── config.toml
```

File: `__init__.py`

```python
from flask_imp import Blueprint

bp = Blueprint(__name__)

bp.import_resources("routes")
bp.import_models("models")
bp.import_nested_blueprints("nested_blueprints")
bp.import_nested_blueprint("standalone_nested_blueprint")


@bp.before_app_request
def before_app_request():
    bp.init_session()
```

That `config.toml` file is loaded during the `__init__` method of the Blueprint class.
To see more about the config file see: [Blueprint / config.toml](blueprint-config-toml.html)

`import_resources` method will walk one level deep into the `routes` folder, and import all `.py` files as modules.
For more information see: [Blueprint.x / import_resources](blueprint_x-import_resources.html)

`import_models` works the same as `imp.import_models`, it will look for instances of `db.Model` and import them. These
will also be available in the model lookup method `imp.model`.
For more information see: [Imp.x / import_models](imp_x-import_models.html)

`import_nested_blueprints` will do the same as `imp.import_blueprints`, but will register the blueprints found as
nested to the current blueprint. For example `www.blueprint_one.index`

`import_nested_blueprint` behaves the same as `import_nested_blueprints`, but will only import a single blueprint.

`bp.init_session` will load the session variables from the config file into the session object. For more information
see: [Blueprint.x / init_session](blueprint_x-init_session.html) and
[Blueprint / config.toml](blueprint-config-toml.html)
