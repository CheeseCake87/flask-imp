from dataclasses import dataclass


@dataclass
class Resources:
    # Format to: secret_key
    default_config = """\
# Flask-BigApp Config File
#
# Updates the Flask app config with the variables below.
# If any variable below does not exist in the standard Flask env vars it is created and will be accessible using
# app.config["YOUR_VAR_NAME"]. All key names defined below will be capitalised when imported.
#
[FLASK]
APP_NAME = "app"
VERSION = "0.0.1"
SECRET_KEY = "change_me"
DEBUG = false
TESTING = false
SESSION_TIME = 480
ERROR_404_HELP = true
SQLALCHEMY_TRACK_MODIFICATIONS = false
EXPLAIN_TEMPLATE_LOADING = false


[DATABASE]
#
# [database.main] is loaded as SQLALCHEMY_DATABASE_URI
# type = mysql / postgresql / sqlite
# if type = sqlite, config parser will ignore username and password
#
[DATABASE.MAIN]
ENABLED = true
TYPE = "sqlite"
DATABASE_NAME = "database"
LOCATION = "db"
PORT = ""
USERNAME = "user"
PASSWORD = "password"

# Adding another database is as simple as adding a new section
# [DATABASE.ANOTHER] will then be accessible using SQLALCHEMY_BINDS
# The bind key will be stored as a lowercase value, so "ANOTHER" will
# be accessible as "another"
# You can then use the bind key in the model as follows:
# class MyModel(db.Model):
#     __bind_key__ = "another"
#     ...
#
#[DATABASE.ANOTHER]
#ENABLED = true
#TYPE = "sqlite"
#DATABASE_NAME = "database_another"
#LOCATION = "db"
#PORT = ""
#USERNAME = "user"
#PASSWORD = "password"
#
# You can add as many databases as you want.\
"""
    # Format to: static_url_path
    default_theme_config = """\
enabled = "yes"
static_folder = "static"
static_url_path = "{static_url_path}"\
"""
