# ImpBlueprint.import_resources

```python
def import_resources(
    folder: str = "resources",
    factories: t.Optional[t.List[str], str] = "include",
    scope_import: t.Optional[
        t.Dict[str, t.Union[t.List[str], str]]
    ] = None
) -> None:
```

---

Will import all the resources (cli, routes, filters, context_processors...)
from the given folder wrapped by the defined factory/factories.

The given folder must be relative to the root of the blueprint.

`folder` the folder to import from - must be relative

`factories` a list of or single function name(s) to pass the blueprint
instance to and call. Defaults to "include"

`scope_import` a dict of files to import e.g. `{"folder_name": "*"}`

**Examples:**

```python
bp = ImpBlueprint(__name__, ImpBlueprintConfig(...))

bp.import_resources(folder="resources")
# or
bp.import_resources()
# as the default folder is "resources"
```

Here's an example blueprint folder structure:

```text
my_blueprint
├── user_routes
│   ├── user_dashboard.py
│   └── user_settings.py
├── static/...
├── templates/
│   └── my_blueprint/
│       ├── user_dashboard.html
│       └── ...
├── __init__.py
```

File: `user_routes/user_dashboard.py`

```python
from flask_imp import ImpBlueprint
from flask import render_template

def include(bp: ImpBlueprint):
    @bp.route("/")
    def user_dashboard():
        return render_template("user_dashboard.html")
```

## How factories work

Factories are the names of functions that are called when importing the resource.
The default factory is `include`, Here's an example of changing the default:

```python
bp.import_resources(
    folder="resources",
    factories="development"
)
```

`"development"` => `development(app)` function will be called, and the current app will be passed in.

File: `user_routes/user_settings.py`

```python
def development(bp: ImpBlueprint):
    @bp.cli.command("reset-user-settings")
    def reset_user_settings():
        print("reset-user-settings cli command")
```

A list of factories can be passed in:

```python
bp.import_resources(
    folder="resources",
    factories=["development", "production"]
)
```

```python
def development(bp: ImpBlueprint):
    @bp.cli.command("reset-user-settings")
    def reset_user_settings():
        print("reset-user-settings cli command")

def production(bp: ImpBlueprint):
    @bp.cli.command("show-user-settings")
    def show_user_settings():
        print("show-user-settings cli command")
```

This feature can be useful to feature flag certain resources.

## Scoping imports

All files and folders will be imported by default. Here's an example of how to scope to
specific folders or files:

```python
bp.import_resources(scope_import={"*": ["cli.py"]})
```

This will import the file `cli.py` from any folder found in the `resources` folder.

```text
my_blueprint/
├── resources/
│   ├── clients/
│   │   ├── cli.py
│   │   └── other.py <- Will not be included
│   └── database/
│       └── cli.py
└── ...
...
```

This will only import the file named `cli.py` from the `clients` folder:

```python
scope_import={"clients": ["cli.py"]}
```

This will only import from the `resouces` folder itself, and skip any other folder:

```python
scope_import={".": ["cli.py"]}
```
