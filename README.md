# Flask-Launchpad - Example / Test Project

To install Flask-Launchpad do:
```
pip install Flask-Launchpad
```

This project imports Flask-Launchpad from a local directory, for testing, obviously.

Flask-Launchpad is a small auto importer to import multiple blueprints and their routes. Can also handle multiple 
imports of flask_restx apis.

This extension allows you to make multiple route files and not have to worry about manually importing each of them.

!BEWARE! - This is an auto importer! - This can be a security concern!
Don't get lazy and ensure you know what code you are potentially going to run. 
(don't auto import files you've not looked at)

Here's an example of how your project should look
```
Example folder structure :
```
```
project/
    - main/
        - blueprints/
            - example/
                - templates/
                - static/
                - routes/
                    - app_info.py
                    - main.py
                - __init__.py
                - config.toml
        - api/
            - v1/
                - functions/
                    api_auth.py
                - routes/
                    test.py
                    test2.py
                - __init__.py
                - config.toml
        - builtins/
            - routes/
                - system.py
            - template_filters/
                - filters.py
        - models/
            - example.py
        - structures/
            - fl_default/
                - css/
                    - main.css
                - error_pages/
                    - 404.html
                - extends/
                    - main.html
                - img/
                    - Flask-Launchpad.png
                - includes/
                    - footer.html
                - js/
                    - main.js
        - __init__.py
        - app_config.toml
        - templates/
        - static/
    - venv/
    - run.py
```
```
main/__init__.py :
```
```python
from flask import Flask
from flask_launchpad import FlaskLaunchpad

fl = FlaskLaunchpad()


def create_app():
    main = Flask(__name__)
    fl.init_app(main)
    fl.app_config("app_config.toml")
    fl.models_folder("models")

    fl.register_structure_folder("structures")

    fl.import_builtins("builtins/routes")
    fl.import_builtins("builtins/template_filters")

    fl.import_apis("api")
    fl.import_blueprints("blueprints")

    return main

```
```text
.app_config() loads Flask env vars, database settings and email settings from a 
specified toml file that sits in the app root folder.

.models_folder() loads model files and classes into the apps config under current_app.config["MODELS"] setting this
in the app __init__.py is optional, and can be set in Blueprint config files if you would rather keep your models
attached to your Blueprints.

.register_structure_folder() registers a cut down Blueprint that will be added to the template folder lookups.

.import_builtins() imports basically app level routes that use @current_app.whatever, this
can be used to import routes and template_filters for jinja as shown.

.import_blueprints() and .import_apis() look in the folder passed in for Blueprint modules and registers them in
Flask. This also includes model files by adding models_folder to the Blueprint config.
```
```
main/blueprints/example/app_config.toml :
```
```toml
# Updates the Flask app config with the variables below.
# If any variable below does not exist in the standard Flask env vars it is created and will be accessible using
# current_app.config["YOUR_VAR_NAME"] or of course, app.config["YOUR_VAR_NAME"] if you are not using app factory.

[flask]
app_name = "main"
version = "0.6.0"
secret_key = "sdflskjdflksjdflksjdflkjsdf"
debug = true
testing = true
session_time = 480
static_folder = "builtins/static"
template_folder = "builtins/templates"
error_404_help = true
SQLALCHEMY_TRACK_MODIFICATIONS = false
structure = "fl_default"
EXPLAIN_TEMPLATE_LOADING = true
login_dashboard = "administrator.users"

# [database.main] is loaded as SQLALCHEMY_DATABASE_URI
# type = mysql / postgresql / sqlite
# if type = sqlite, config parser will ignore username and password
[database]

    [database.main]
    enabled = true
    type = "sqlite"
    server = "local"
    database_name = "database"
    username = "user"
    password = "password"

# works well with Microsoft Exchange Kiosk License
# for Exchange Kiosk to work you must enable Authenticated-SMTP in the accounts features
# this feature takes a while to activate, so don't expect instant results
# The name of the key is used as the username to login to the server defined below.
# If your username is different uncomment alt_username and set it there
[smtp]

    [smtp."email@email.com"]
    enabled = false
    password = "password"
    server = "smtp-mail.outlook.com"
    port = 587
    send_from = "email@emial.com"
    reply_to = "email@emial.com"
    #alt_username = "username"

    [smtp."email2@email.com"]
    enabled = false
    password = "password"
    server = "smtp-mail.outlook.com"
    port = 587
    send_from = "email@emial.com"
    reply_to = "email@emial.com"
    #alt_username = "username"

```
```
main/blueprints/example/__init__.py :
```
```python
from flask import session
from flask import current_app

from flask_launchpad import FLStructure
from flask_launchpad import FLBlueprint

fl_bp = FLBlueprint()
bp = fl_bp.register()

fls = FLStructure(current_app, current_app.config["STRUCTURE"])

fl_bp.import_routes("routes")


@bp.before_app_first_request
def before_app_first_request():
    pass


@bp.before_app_request
def before_app_request():
    for key in fl_bp.session:
        if key not in session:
            session.update(fl_bp.session)
            break


@bp.after_app_request
def after_app_request(response):
    return response


```
```
main/blueprints/example/config.toml :
```
```toml
[init]
enabled = true
version = 0.1

[settings]
type = "blueprint"
models_folder = "models"
# models_folder is optional, see app __init__.py above for more info

[blueprint]
url_prefix = "/example"
template_folder = "templates"
static_folder = "static"
static_url_path = "/static"

[session]
var_in_session = "this can be loaded using fl_bp.session"

```
```
main/blueprints/example/routes/app_info.py :
```
```python
from flask import current_app

from .. import fls
from .. import bp


@bp.route("/app-models", methods=["GET"])
def app_models():
    output = ""
    for key, value in current_app.config["models"].items():
        output += f"{key} : {value} <br/>"
    return output


@bp.route("/app-url-map", methods=["GET"])
def app_url_map():
    output = ""
    for rule in current_app.url_map.iter_rules():
        output += f"{rule.endpoint} : {rule.rule} <br/>"
    return output
```

import_apis() from the main / init file, works much the same as the blueprint imports, although it prepends the blueprint holding folder into the URL registration.

In this example the v1 API folder with be registered against /api/v1

Here's an example of how the files should look to register APIs

```
main/api/v1/__init__.py :
```
```python
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask import session

from flask_launchpad import FLBlueprint

fl_bp = FLBlueprint()

api_bp = fl_bp.register()
api = Api(api_bp, doc=f"/docs")

fl_bp.import_routes()
# import_routes() defaults to a folder called routes

db = SQLAlchemy()
sql_do = db.session


@api_bp.before_app_first_request
def before_app_first_request():
    pass


@api_bp.before_app_request
def before_app_request():
    for key in fl_bp.session:
        if key not in session:
            session.update(fl_bp.session)
            break


@api_bp.after_app_request
def after_app_request(response):
    return response
```
```
main/api/v1/config.toml :
```
```toml
[init]
enabled = true
version = 1.0

[settings]
type = "api"
models_folder = "folder"

[blueprint]
url_prefix = "/v1"

[http_auth]
enabled = false
http_user = "httpuser"
http_pass = "httppass"

[public_key]
enabled = false
public_key = "a3oe3qhY8knm"
```
```
main/api/v1/routes/test.py :
```
```python
from ..functions.api_auth import public_key_required
from flask_restx import Resource

from .. import api


@api.route('/test')
class Test(Resource):
    def get(self):
        return "GET Method"

    def post(self, public_key):
        public_key_required(public_key)
        return """POST Method"""
```

Sticking to this method of blueprints and APIs will allow you to mass import route files.
