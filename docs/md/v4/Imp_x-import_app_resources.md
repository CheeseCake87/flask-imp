```
Menu = Imp.x/import_app_resources
Title = Imp.import_app_resources
```

```python
import_app_resources(
    folder: str = "resources",
    factories: Optional[List] = None,
    static_folder: str = "static",
    templates_folder: str = "templates",
    files_to_import: Optional[List] = None,
    folders_to_import: Optional[List] = None,
    ) -> None
```

---

Import standard app resources from the specified folder.

This will import any resources that have been set to the Flask app.

Routes, context processors, cli, etc.

**Can only be called once.**

If no static and or template folder is found, the static and or template folder will be set to None in the Flask app
config.

#### Small example of usage:

```python
imp.import_app_resources(folder="resources")
# or
imp.import_app_resources()
# as the default folder is "resources"
```

Folder Structure: `resources`

```text
app
├── resources
│   ├── routes.py
│   ├── app_fac.py
│   ├── static
│   │   └── css
│   │       └── style.css
│   └── templates
│       └── index.html
└── ...
...
```

File: `routes.py`

```python
from flask import current_app as app
from flask import render_template


@app.route("/")
def index():
    return render_template("index.html")
```

#### How factories work

Factories are functions that are called when importing the app resources. Here's an example:

```python
imp.import_app_resources(
    folder="resources",
    factories=["development_cli"]
)
```

`["development_cli"]` => `development_cli(app)` function will be called, and the current app will be passed in.

File: `app_fac.py`

```python
def development_cli(app):
    @app.cli.command("dev")
    def dev():
        print("dev cli command")
```

#### Scoping imports

By default, all files and folders will be imported.

To disable this, set `files_to_import` and or
`folders_to_import` to `[None]`.

```python
imp.import_app_resources(files_to_import=[None], folders_to_import=[None])
```

To scope the imports, set the `files_to_import` and or `folders_to_import` to a list of files and or folders.

`files_to_import=["cli.py", "routes.py"]` => will only import the files `resources/cli.py`
and `resources/routes.py`

`folders_to_import=["template_filters", "context_processors"]` => will import all files in the folders
`resources/template_filters/*.py` and `resources/context_processors/*.py`
