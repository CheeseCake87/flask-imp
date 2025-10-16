# Imp.import_resources

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

The given folder must be relative to the root of the app.

`folder` the folder to import from - must be relative

`factories` a list of or single function name(s) to pass the app
instance to and call. Defaults to "include"

`scope_import` a dict of files to import e.g. `{"folder_name": "*"}`

**Examples:**

```python
imp.import_resources(folder="resources")
# or
imp.import_resources()
# as the default folder is "resources"
```

Folder Structure: `resources`

```text
app
├── resources
│   ├── routes.py
│   └── app_fac.py
└── ...
...
```

File: `routes.py`

```python
from flask import Flask
from flask import render_template

def include(app: Flask):
    @app.route("/")
    def index():
        return render_template("index.html")
```

## How factories work

Factories are the names of functions that are called when importing the resource.
The default factory is `include`, Here's an example of changing the default:

```python
imp.import_resources(
    folder="resources",
    factories="development"
)
```

`"development"` => `development(app)` function will be called, and the current app will be passed in.

File: `app_fac.py`

```python
def development(app: Flask):
    @app.cli.command("dev")
    def dev():
        print("dev cli command")
```

A list of factories can be passed in:

```python
imp.import_resources(
    folder="resources",
    factories=["development", "production"]
)
```

```python
def development(app: Flask):
    @app.cli.command("dev")
    def dev():
        print("dev cli command")

def production(app: Flask):
    @app.cli.command("create-db")
    def prod():
        print("create-db cli command")
```

This feature can be useful to feature flag certain resources.

## Scoping imports

All files and folders will be imported by default. Here's an example of how to scope to
specific folders or files:

```python
imp.import_resources(scope_import={"*": ["cli.py"]})
```

This will import the file `cli.py` from any folder found in the `resources` folder.

```text
app/
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
