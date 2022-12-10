from dataclasses import dataclass


@dataclass
class Resources:
    default_config = """
# Updates the Flask app config with the variables below.
# If any variable below does not exist in the standard Flask env vars it is created and will be accessible using
# app.config["YOUR_VAR_NAME"]. All variables defined below will be capitalised when imported.

[flask]
APP_NAME = "app"
VERSION = "0.0.1"
SECRET_KEY = "changeme"
DEBUG = true
TESTING = true
SESSION_TIME = 480
ERROR_404_HELP = true
SQLALCHEMY_TRACK_MODIFICATIONS = false
EXPLAIN_TEMPLATE_LOADING = false

# [database.main] is loaded as SQLALCHEMY_DATABASE_URI
# type = mysql / postgresql / sqlite
# if type = sqlite, config parser will ignore username and password
[database]

    [database.main]
    enabled = true
    type = "sqlite"
    database_name = "database"
    location = "db"
    port = ""
    username = "user"
    password = "password"

"""
