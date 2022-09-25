![](https://raw.githubusercontent.com/CheeseCake87/Flask-BigApp/master/app/structures/bigapp_default/static/img/Flask-BigApp-Logo-white-bg.png)

# Flask-BigApp

```bash
pip install flask-bigapp
```

![Tests](https://github.com/CheeseCake87/Flask-BigApp/actions/workflows/tests.yml/badge.svg)

`NOTE:` This version; Being 1.2.* and above includes some breaking changes from anything on version 1.1.*

## What is Flask-BigApp?

Flask-BigApp's main purpose is to help simplify the importing of blueprints, routes and models.
It has a few extra features built in to help with theming, securing pages and password authentication.

## Minimal Flask-BigApp app

A config file is required to sit next to your app's ```__init__.py``` file. This defaults to ```default.config.toml```

If Flask-BigApp is unable to find the `default.config.toml` file, it will create one.

You can also set the config file by setting the `BA_CONFIG` environment variable.
For example: (in terminal) `export BA_CONFIG=production.config.toml`

The ```default.config.toml``` file contains Flask config settings, a minimal version of this file looks like this:

```toml
# Updates the Flask app config with the variables below.
# If any variable below does not exist in the standard Flask env vars it is created and will be accessible using
# current_app.config["YOUR_VAR_NAME"] or of course, app.config["YOUR_VAR_NAME"] if you are not using app factory.

[flask]
app_name = "app"
version = "0.0.0"
secret_key = "sdflskjdflksjdflksjdflkjsdf"
debug = true
testing = true
session_time = 480
static_folder = "static"
template_folder = "templates"
error_404_help = true
```

You can also use environment variables markers in the config file, here's an example:

```toml
# Updates the Flask app config with the variables below.
# If any variable below does not exist in the standard Flask env vars it is created and will be accessible using
# current_app.config["YOUR_VAR_NAME"] or of course, app.config["YOUR_VAR_NAME"] if you are not using app factory.

[flask]
app_name = "app"
version = "0.0.0"
secret_key = "<SECRET_KEY>"
debug = "<DEBUG>"
testing = true
session_time = 480
static_folder = "static"
template_folder = "templates"
error_404_help = true
random_value = "<TAGS_CAN_BE_ANYTHING>"
```

Now if you set environment variables that are included in the tags, Flask-BigApp will replace them with the values.
Here's an example of setting environment variables in linux:

`export SECRET_KEY="asdlasijd90339480239oiqjdpiasdj"` and `export DEBUG=True`

The environment variables to pass in are defined in the config file, have a look at `random_value`.
To set this we will need to do: `export TAGS_CAN_BE_ANYTHING="what we put here will be the new value"`

**NOTE:** Some environment variable tags in the config file may not work if you are using `flask run`,
you can run the app by using `venv/bin/python run_example.py` instead.

Your app's ```__init__.py``` file should look like this:

```python
from flask import Flask
from flask_bigapp import BigApp

bigapp = BigApp()


def create_app():
    main = Flask(__name__)
    bigapp.init_app(main)
    bigapp.import_builtins("routes")
    return main
```

**NOTE:** You can also manually set the config file by doing `bigapp.init_app(main, app_config_file="dev.config.toml")`

The ```bigapp.import_builtins("routes")``` method looks in the ```routes``` folder for ```.py``` files to import app routes
from.

Let's say we have this folder structure:

```
Flask-BigApp
|
- app/
-- static/
-- templates/
--- routes/
------ index.py
-- __init__.py
-- app_config.toml
- venv
- run.py
```

The ```index.py``` file should look like this:

```python
from flask import current_app


@current_app.route("/", methods=['GET'])
def index_page():
    """
    Example index route
    """
    return "You will see this text in the browser"
```

This file will get imported into the main app using the ```import_builtins()```method.

This is also the case if we add another file into the ```routes``` folder. Let's say we add ```my_page.py``` into the
routes folder, and it looks like this:

```python
from flask import current_app


@current_app.route("/my-page", methods=['GET'])
def my_page():
    """
    My Page Route
    """
    return "This is my page route"
```

So now our folder structure looks like this:

```
Flask-BigApp
|
- app/
-- static/
-- templates/
--- routes/
------ index.py
------ my_page.py
-- __init__.py
-- app_config.toml
- venv
- run.py
```

The ```my_page.py``` routes will also be imported into the main app.

Using this method you can keep your routes in different files, and not have to worry about adding the import into
your ```__init__.py``` file.


## Setting up to work with models using SQLAlchemy

To work with models using SQLAlchemy, your app `__init__.py` file should look like this:

```python
from flask import Flask
from flask_bigapp import BigApp
from flask_sqlalchemy import SQLAlchemy

bigapp = BigApp()
db = SQLAlchemy()


def create_app():
    main = Flask(__name__)
    bigapp.init_app(main, db)  # Here we are passing in the SQLAlchemy object.
    bigapp.import_builtins("routes")
    return main
```

Giving Flask-BigApp the database object will auto init the model files 
and load a registry of models that can then be accessed from the model_class method.
See Importing Models below, for more information.

The database settings can either be added by setting the flask-sqlalchemy 
app config manually `main.config['SQLALCHEMY_DATABASE_URI'] = WHATEVER_URI` or by
including the settings your config file. Here's an example:

```toml
[flask]
app_name = "app"
version = "0.0.0"
secret_key = "sdflskjdflksjdflksjdflkjsdf"
debug = true
testing = true
session_time = 480
static_folder = "static"
template_folder = "templates"
error_404_help = true

[database]
    [database.main]
    enabled = true
    type = "sqlite"
    database_name = "database"
    location = "db"
    port = ""
    username = "user"
    password = "password"
```

`NOTE:` The only accepted types of databases are: mysql / postgresql / sqlite / oracle

Flask-BigApp will also handle any binds. Any database settings added after the database.main section, will be added as a bind.

```toml
...
[database]
    [database.main]
    enabled = true
    type = "sqlite"
    database_name = "database"
    location = "db"
    port = ""
    username = "user"
    password = "password"

    [database."defined_name"]
        enabled = true
        type = "sqlite"
        database_name = "other_database"
        location = "db"
        port = ""
        username = "user"
        password = "password"
```

This is the same as the configuration:

```text
SQLALCHEMY_DATABASE_URI = 'sqlite:////absolute_app_path/db/database.sqlite'
SQLALCHEMY_BINDS = {
    'defined_name': 'sqlite:////absolute_app_path/db/other_database.sqlite',
}
```



## Importing Models

You can import model classes from a single file, of a folder of 
model files by using the `bigapp.import_models(file="models.py", folder="models")` method.

Here's an example of how you can setup Flask-BigApp to import model classes:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bigapp import BigApp

bigapp = BigApp()
db = SQLAlchemy()


def create_app():
    main = Flask(__name__)
    bigapp.init_app(main, db)  # Here we are passing in the SQLAlchemy object.
    bigapp.import_builtins("routes")
    bigapp.import_models(file="models.py")
    # OR
    bigapp.import_models(folder="models")
    # OR
    bigapp.import_models(file="models.py", folder="models")
    return main
```

## Model Files

Here's an example of what a model file looks like:


```python
from app import bigapp
from sqlalchemy import ForeignKey

db = bigapp.db


class ExampleTable(db.Model):
    __tablename__ = "fl_example_table"
    example_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('fl_example_user.user_id'))
    thing = db.Column(db.String(256), nullable=False)
```

## Working with the model_class method

Here's an example of how you can query using the `bigapp.model_class` method:
( this assumes you have `bigapp = BigApp()` in your apps `__init__.py` file )

```python
from flask import render_template

from app import bigapp
from .. import bp


@bp.route("/database-example", methods=["GET"])
def database_example():
    # Load the ExampleUser class found in the import_models folder, this way saves having to import files
    example_user = bigapp.model_class("ExampleUser")

    user_id = 1
    result = "NULL"
    find_username = True

    # Normal query
    nq_example_user = example_user.query

    # Query class using sql_do session
    sq_example_user = bigapp.sql_do.query(example_user)

    if find_username:
        sq_example_user = sq_example_user.filter(example_user.user_id == user_id).first()
        if sq_example_user is not None:
            username = sq_example_user.username
            result = f"Session Query: Username is {username}"

        nq_example_user = nq_example_user.filter(example_user.user_id == user_id).first()
        if nq_example_user is not None:
            username = nq_example_user.username
            example_table_join = nq_example_user.rel_example_table[0].thing
            result = f"{result}, Normal Query: Username is {username} -> ExampleTable Join: {example_table_join}"

    render = "blueprint1/database-example.html"
    return render_template(render, result=result)
```

The `bigapp.sql_do` method is just a proxy for `db.session`

## Importing Builtins (routes, template filters, context processors)

You can auto import routes, template filters, context processors, etc.. from a folder using:

- `bigapp.import_builtins("builtins")`

Here's an example of the builtins folder structure:

```text
builtins/
|
-- routes.py
-- template_filters.py
```

Importing builtins uses Flask's `current_app` to register the routes, here's an example of a file in the builtins folder:

```python
from flask import current_app
from flask import Response
from flask import render_template
from markupsafe import Markup


@current_app.template_filter('example')
def decorate_code(value: str) -> str:
    return Markup(f"The string value passed in is: {value} -> here is something after that value.")


@current_app.before_request
def before_request():
    pass


@current_app.errorhandler(404)
def request_404(error):
    return Response(error, 404)


@current_app.route("/builtin/route")
def builtin_route():
    render = "theme1/renders/builtin-route.html"
    return render_template(render)
```

## Importing Blueprints

You can auto import blueprints using:

- `bigapp.import_blueprints("blueprints")`

The shape of your folder to import blueprints from should look like this:

```text
blueprints/
|
- blueprint1/
-- routes/
---- index.py
-- templates/
---- blueprint1/
------ index.html
-- static/
-- __init__.py
-- config.toml
|
- another_blueprint/
-- routes/
---- index.py
-- templates/
---- another_blueprint/
------ index.html
-- static/
-- __init__.py
-- config.toml
```

In the above we are nesting all templates under a folder with the same name as the blueprint. This is a workaround to allow you to have template files with the
same names in different blueprint folders.

Blueprints require a config file to configure their settings. The config file should look like this:

```toml
enabled = "yes"

[settings]
url_prefix = "/"
template_folder = "templates"
static_folder = "static"
static_url_path = "/blueprint1/static"

[session]
var_in_session = "this can be loaded using bp.init_session()"
permissions = ["this", "that"]
logged_in = true
not_logged_in = false
```

The session section can be initialised using the `bp.init_session()` method. This places the values into the Flask session -> `from flask import session`

Here's an example of what your blueprints `__init__.py` file should look like:

```python
from flask_bigapp import Blueprint

bp = Blueprint(__name__, "config.toml")

bp.import_routes("routes")


@bp.before_app_request
def before_app_request():
    bp.init_session()


@bp.after_app_request
def after_app_request(response):
    return response
```

Flask-BigApp inherits from Flask's Blueprint class in order to load from the config file. In the example above it states the config file name, however you can
omit this as it defaults to `config.toml`. Of course, you can specify your own config file name.

`bp.import_routes("routes")` method works much the same as `bigapp.import_builtins` except it is scoped to work with the blueprint object.

Here's an example of `routes/index.py`

```python
from flask import render_template

from .. import bp


@bp.route("/", methods=["GET"])
def index():
    render = bp.tmpl("index.html")

    return render_template(render)
```

The `bp.tmpl` method just decorates the string with the name of the blueprint, changing `"index.html"` to `"blueprint1/index.html"`.

Of course this only works if your templates are nested under a folder with the same name as your blueprint, however it does make it possible to change the
blueprint name later and not have to worry about search and replace.

## Importing Structures (themes)

You can register a structures (theme) folder using:

- `bigapp.import_structures("structures")`

Structures work the same as blueprints but are used for theming and do not have a config file, here's an example of the folder layout of the structures folder:

```text
structures/
|
- theme1/
-- templates/
--- theme1/
---- extend/
------ main.html
---- includes/
------ footer.html
---- macros/
------ theme1_menu.html
-- static/
---- logo.png
---- style.css
-- __init__.py
-- config.toml
```

# GitHub Project

This github project is a working example, and can do much more than the minimal app above.

This project covers how to work with models, blueprints and themes (structures)

### Linux setup

(Assuming location is home directory)

#### Git clone:

```bash
git clone https://github.com/CheeseCake87/Flask-BigApp.git
```

**OR**

1. Download zip and unpack
2. cd into unpacked folder

---
Move into the Flask-BigApp directory:

```bash
cd Flask-BigApp
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Enter virtual environment:

```bash
source venv/bin/activate
```

Install Flask-BigApp from src:

```bash
pip install -e .
```

Run Flask:

```bash
flask run
```

Or run from file:

```bash
python3 run_example.py
```
