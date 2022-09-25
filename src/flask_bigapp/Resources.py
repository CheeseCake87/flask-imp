from dataclasses import dataclass


@dataclass
class Resources:
    default_config = """
# Updates the Flask app config with the variables below.
# If any variable below does not exist in the standard Flask env vars it is created and will be accessible using
# current_app.config["YOUR_VAR_NAME"] or of course, app.config["YOUR_VAR_NAME"] if you are not using app factory.

[flask]
app_name = "app"
version = "0.0.1"
secret_key = "changeme"
debug = true
testing = true
session_time = 480
error_404_help = true
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

# works well with Microsoft Exchange Kiosk License
# for Exchange Kiosk to work you must enable Authenticated-SMTP in the accounts features
# this feature takes a while to activate, so don't expect instant results
# The name of the key is used as the username to login to the server defined below.
# If your username is different uncomment alt_username and set it there
[smtp]

    [smtp."email_address"]
    enabled = false
    password = "password"
    server = "smtp-mail.outlook.com"
    port = 587
    send_from = "email@emial.com"
    reply_to = "email@emial.com"
    #alt_username = "username"

    [smtp."email_address_2"]
    enabled = false
    password = "password"
    server = "smtp-mail.outlook.com"
    port = 587
    send_from = "<EMAIL_ADDRESS>"
    reply_to = "email@emial.com"
    #alt_username = "username"
"""
