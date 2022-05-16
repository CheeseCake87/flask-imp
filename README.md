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

project/
    - main/
        - blueprints/
            - example/
                - routes/
                    - route1.py
                    - route2.py
                - __init__.py
                - config.toml
                - models.py
            - example2/
            - example3/
        - api/
            - v1/
                - routes/
                    api_route1.py
                    api_route2.py
                - __init__.py
                - config.toml
                - models.py
                
        - __init__.py
        - app_config.toml
    - venv/
    - run.py
```
```
main/__init__.py :
```
```python
from flask import Flask
from flask_launchpad import FlaskLaunchpad

# ~~ other imports

fl = FlaskLaunchpad()

def create_app():
    main = Flask(__name__)
    fl.init_app(main)
    fl.app_config("app_config.toml")
    fl.import_builtins("routes")
    fl.import_builtins("another/folder/template_filters")
    fl.import_blueprints("blueprints")
    fl.import_apis("api")

# ~~~ other create app things

```

.app_config() loads Flask env vars, database settings and email
settings from a specified toml file that sits in the app root folder

.import_builtins() imports basically app level routes that use @current_app.whatever, this
can be used to import routes and template_filters for jinja as shown.
```
main/blueprints/example/app_config.toml :
```
```toml
# Updates the Flask app config with the variables below.
# If any variable below does not exist in the standard Flask env vars it is created and will be accessible using
# current_app.config["YOUR_VAR_NAME"] or of course, app.config["YOUR_VAR_NAME"] if you are not using app factory.

[flask]
name = "main"
secret_key = "sdflskjdflksjdflksjdflkjsdf"
debug = true
testing = true
session_time = 480
static_folder = "static"
template_folder = "templates"
error_404_help = true
SQLALCHEMY_TRACK_MODIFICATIONS = false

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

    # Anything below will be imported using SQLALCHEMY_BINDS, with the [SECTION] name being the __bind_key__

    [database.example1]
    enabled = false
    type = "mysql"
    server = "0.0.0.0"
    database_name = "example1"
    username = "user"
    password = "password"

    [database.example2]
    enabled = false
    type = "mysql"
    server = "localhost"
    database_name = "example2"
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
from flask_launchpad import FLBlueprint

fl_bp = FLBlueprint()
bp = fl_bp.register()
fl_bp.import_routes("routes")
```
```
main/blueprints/example/config.toml :
```
```toml
[init]
enabled = true
version = 0.1
type = "blueprint"

[settings]
url_prefix = "/example"
template_folder = "templates"
static_folder = "static"
static_url_path = "/static"

```
```
main/blueprints/example/routes/route1.py :
```
```python
from .. import bp


@bp.route("/", methods=["GET"])
def index():
    """Example of route url redirect"""
    return """Working..."""
```

import_apis() from the main / init file, works much the same as the blueprint imports, although it prepends the blueprint holding folder into the URL registration.

In this example the v1 API folder with be registered against /api/v1

Here's an example of how the files should look to register APIs

```
main/api/v1/__init__.py :
```
```python
from flask_restx import Api
from flask_launchpad import FLBlueprint

fl_bl = FLBlueprint()
api_bp = fl_bl.register()
api = Api(api_bp, doc=f"/docs")
fl_bl.import_routes()
# import_routes() defaults to a folder called routes
```
```
main/api/v1/config.toml :
```
```toml
[init]
enabled = true
version = 1.0
type = "api"

[settings]
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
main/api/v1/routes/api_route1.py :
```
```python
from flask_restx import Resource

from .. import api


@api.route('/test')
class Test(Resource):
    def get(self):
        return "waiting"
```

Sticking to this method of blueprints and APIs will allow you to mass import route files.

It also auto imports models.py files, this does need a little more dev though.