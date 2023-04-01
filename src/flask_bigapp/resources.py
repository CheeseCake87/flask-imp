from dataclasses import dataclass


@dataclass
class Resources:
    # Format to: secret_key
    default_config = """\
# Updates the Flask app config with the variables below.
# If any variable below does not exist in the standard Flask env vars it is created and will be accessible using
# app.config["YOUR_VAR_NAME"]. All variables defined below will be capitalised when imported.

[FLASK]
APP_NAME = "app"
VERSION = "0.0.1"
SECRET_KEY = "<CONFIG_SECRET_KEY>"
DEBUG = false
TESTING = false
SESSION_TIME = 480
ERROR_404_HELP = true
SQLALCHEMY_TRACK_MODIFICATIONS = false
EXPLAIN_TEMPLATE_LOADING = false

# [database.main] is loaded as SQLALCHEMY_DATABASE_URI
# type = mysql / postgresql / sqlite
# if type = sqlite, config parser will ignore username and password
[DATABASE]
[DATABASE.MAIN]
ENABLED = true
TYPE = "sqlite"
DATABASE_NAME = "database"
LOCATION = "db"
PORT = ""
USERNAME = "user"
PASSWORD = "password"

"""
    # Format to: static_url_path
    default_theme_config = """\
enabled = "yes"
static_folder = "static"
static_url_path = "{static_url_path}"
"""
