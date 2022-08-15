# Flask-BigApp

```bash
pip install flask-bigapp
```

---

## Contents

[What is Flask-BigApp?](#What is Flask-BigApp?)

[Minimal Flask-BigApp app](#Minimal Flask-BigApp app)

[Working with Models](#Working with Models)

[Setup GitHub version](#Setup GitHub version)

[Setup GitHub version](#Setup GitHub version)

[Setup GitHub version](#Setup GitHub version)

---
## What is Flask-BigApp?

Flask-BigApp's main purpose is to help simplify the importing of blueprints, templates and models.

It has a few extra features built in to help with theming, securing pages and password authentication.

---


## Minimal Flask-BigApp app

```app_config.toml``` file is required to sit next to your app's ```__init__.py``` file.

The ```app_config.toml``` file contains Flask config settings, a minimal version of this file looks like this:

```toml
# Updates the Flask app config with the variables below.
# If any variable below does not exist in the standard Flask env vars it is created and will be accessible using
# current_app.config["YOUR_VAR_NAME"] or of course, app.config["YOUR_VAR_NAME"] if you are not using app factory.

[flask]
app_name = "main"
version = "0.0.0"
secret_key = "sdflskjdflksjdflksjdflkjsdf"
debug = true
testing = true
session_time = 480
static_folder = "static"
template_folder = "templates"
error_404_help = true
```

Your app's ```__init__.py``` file should look like this:

```python
from flask import Flask
from flask_bigapp import BApp

bapp = BApp()


def create_app():
    main = Flask(__name__)
    bapp.init_app(main)
    bapp.app_config("app_config.toml")
    bapp.import_builtins("routes")
    return main
```

The ```bapp.import_builtins("routes")``` method looks in the ```routes``` folder for ```.py``` files to import app routes
from.

Let's say we have this folder structure:

```
Flask-BigApp
    main
        static
        templates
        routes
            index.py
        __init__.py
        app_config.toml
    venv
    run.py
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
    main
        static
        templates
        routes
            index.py
            my_page.py
        __init__.py
        app_config.toml
    venv
    run.py
```

The ```my_page.py``` routes will also be imported into the main app.

Using this method you can keep your routes in different files, and not have to worry about adding the import into
your ```__init__.py``` file.

This is an example of a very basic app in Flask-BigApp.

---

## Working with Models

In your apps `__init__.py` file we will include the `bapp.models` method

```python
from flask import Flask
from flask_bigapp import BApp

bapp = BApp()


def create_app():
    main = Flask(__name__)
    bapp.init_app(main)
    bapp.app_config("app_config.toml")

    # File or Folder can be set
    bapp.models(file="models.py", folder="models_folder")

    bapp.import_builtins("routes")
    return main
```

The `bapp.models` method initializes flask_sqlalchemy into `BApp.db`.

It also loads the classes along with their attributes into `BApp` and can be retrieved
using the `bapp.model_class` method.

Here is what our model file looks like:

```python
from app import bapp

db = bapp.db


class ExampleUser(db.Model):
    __tablename__ = "fl_example_user"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    salt = db.Column(db.String(4), nullable=False)
    private_key = db.Column(db.String(256), nullable=False)
    disabled = db.Column(db.Boolean)
```

Below is an example route using the `bapp.model_class` method:

```python
@bp.route("/database-example", methods=["GET"])
def database_example():
    # Load the ExampleUser class found in the models folder, this way saves having to import files
    example_user = bapp.model_class("ExampleUser")

    user_id = 1
    result = "NULL"
    find_username = True

    # Normal query
    nq_example_user = example_user.query

    # Query class using sql_do session
    sq_example_user = bapp.sql_do.query(example_user)

    if find_username:
        sq_example_user = sq_example_user.filter(example_user.user_id == user_id).first()
        if sq_example_user is not None:
            username = sq_example_user.username
            result = f"Session Query: Username is {username}"

        nq_example_user = nq_example_user.filter(example_user.user_id == user_id).first()
        if nq_example_user is not None:
            username = nq_example_user.username
            result = f"{result}, Normal Query: Username is {username}"

    return f"{result}"
```
`bapp.model_class("ExampleUser")` load the `ExampleUser` class into the variable `example_user` that can then be used to query.

You may have also noticed `bapp.sql_do` this is just a proxy for `db.session`

---

## Working with Blueprints

---


## Setup GitHub version

! This project imports Flask-BigApp from a local directory (_flask_bigapp) !

### Linux setup

(Assuming location is home directory)

#### Git clone:

```bash
git clone https://github.com/CheeseCake87/Flask-BigApp.git
```

```bash
cd Flask-BigApp
```

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

#### Manual:

1. Download zip and unpack
2. cd into unpacked folder

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

---


### Etc...

Please check out the Flask-BigApp GitHub project. It contains working examples of what Flask-BigApp can do, and
how it can be used to save some time with projects that require a lot of importing.

More documentation coming soon!