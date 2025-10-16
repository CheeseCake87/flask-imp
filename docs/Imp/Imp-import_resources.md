# Imp.import_resources

```python
def import_resources(
    folder: str = "resources",
    factories: t.Optional[t.List[str]] = None,
    scope_import: t.Optional[
        t.Dict[str, t.Union[t.List[t.Optional[str]], t.Optional[str]]]
    ] = None,
) -> None:
```

---

Imports app resources from the given folder. Sub folders at one level deep are supported.

Providing a list of factories will overwrite the default factory of "include",
to keep the include factory, add it to the list you provide.

Routes, context processors, cli, etc.

`folder` The folder to import from, must be relative.

`factories` A list of function names to call with the app instance, defaults to `["include"]`.

`scope_import` A dict of files to import e.g. `{"folder_name": "*"}`.

**Small example of usage:**

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

Factories are functions that are called when importing the app resources. Here's an example:

```python
imp.import_resources(
    folder="resources",
    factories=["development_cli"]
)
```

`["development_cli"]` => `development_cli(app)` function will be called, and the current app will be passed in.

File: `app_fac.py`

```python
def development_cli(app: Flask):
    @app.cli.command("dev")
    def dev():
        print("dev cli command")
```

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
