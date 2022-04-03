from ...builtins.functions.import_mgr import load_config
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from os import path

# Get the path of the Blueprint
this_path = path.dirname(path.realpath(__file__))

# Load the Blueprint config
config = load_config(from_file_dir=this_path)

# Create the Blueprint object (root_path needs to be set as the style of auto
# import breaks the auto-detection of template folders)
bp = Blueprint(**config["settings"], root_path=this_path)

# Create the SQLAlchemy object
db = SQLAlchemy()

# Create session object
sql_do = db.session
