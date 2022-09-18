# These are out of date currently, soz

#### contains_illegal_chars

```text
Finds illegal chars in <name>, is able to accept exceptions in list form.
```

#### load_config

```text
This loads a config.toml file from passed in path. Main usage is for blueprint imports.
```

### BApp

```text
Main BigApp Class
```

#### BApp.app_config

```text
Enables the config.toml method to set Flask env vars, deal with custom Flask env vars,
smtp settings, and database settings.
```

#### BApp.import_builtins

```text
This allows you to import app level routes and template_filters.
It does the same as:
from .routes import my_route
But loops the import over all valid files found
```

#### BApp.import_builtins

```text
This method is used to load valid model files, it looks for the attribute "db" in the file then init_apps them
to the main app.

It also puts the import path, import object(io) and the db attribute into:
app.config['MODELS']['modules']['module_nam ']

It also loads the class names found in the file into app.config['MODELS']['classes']['class_name']

See functions model_class() and model_module()

The shape of the config data looks like this:

app.config["MODELS"] {
"modules": { "module_name": {"import": "app.module.location", "io": import_object, "db": getattr("db") }, },
"classes": { "class_name": class_object, }
}
```

#### BApp.create_all_models

```text
This creates the database, tables and fields from the import_models found in current_app.config["MODELS"]
Can be used like:

BigApp(current_app).create_all_models()

~or~

create_app():
    ~~~~
    ba.create_all_models()
```

#### BApp.import_blueprints

```text
Looks through the passed in folder for Blueprint modules; Imports them then registers them with Flask.
The Blueprint object must be stored in a variable called bp in the __init__.py file in the Blueprint folder.
```

#### BApp.import_apis

```text
Looks through the passed in folder for Blueprint modules, imports them then registers them with Flask.
This does the same as import_blueprints, but decorates the blueprint name with an api marker
The Blueprint object must be stored in a variable called api_bp in the __init__.py file in the Api Blueprint folder.
```

#### BApp.model_class

```text
Returns a class object that is stored in app.config, returns error if not found.

See BigApp.models_folder()
```

### BABlueprint

```text
Class that handles Blueprints from within the Blueprint __init__ file
```

#### BABlueprint.register

```text
Pulls the settings from the Blueprints config file and uses them to register a Flask Blueprint.
```

#### BABlueprint.import_routes

```text
Imports the routes from within the Blueprint folder.
```

### BAStructure

```text
This is used for more flexible theming and templating.
I've called this structures and not themes as a template folder can
import template files, macros, etc.

In the app app __init__ file you can do:

sts = BAStructure(current_app, "folder_where_structures_are_stored")

~or~

create_app():
    ~~~~
    sts.init_app(app, "folder_where_structures_are_stored")
```

#### BAStructure.register_structure

```text
Registers a folder in the specified structures folder as a Flask blueprint.
This makes it available to the render_template lookthrough for templates and
url_for("folder.static") for static files
```

#### ClassMethods: BAStructure.extend, BAStructure.include, BAStructure.error_page, BAStructure.render

```text
To use the class methods you will need to structure your structure in a specific way
app_root 
    structures
        structure_name
            static
            templates
                structure_name
                    extends
                    includes
                    errors
                    renders

We need to specify the structure name again under the templates directory, as all template folders
registered by blueprints are all added to the same lookup table, if a template file shares the same name with
another structure or blueprint they would clash.

The methods below make it easy to pull from the template folder of the structure

in a route page:

from app import structures

structure = "name_of_structure_folder"  # this can be stored in a session var to allow theme picking

@bp.route
render_template(<local_bp_template>, extend=sts.extend("template.html", structure)

jinja of local_bp_template:

{% extends extend %}
... rest or page ...
```