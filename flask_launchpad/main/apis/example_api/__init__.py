from ...builtins.functions.import_mgr import load_config
from flask_restx import Api
from os import path
from flask_sqlalchemy import SQLAlchemy

config = load_config(from_file_dir=path.dirname(path.realpath(__file__)))
db = SQLAlchemy()
api = Api(prefix=config["settings"]["url_prefix"], doc=config["settings"]["url_prefix"] + "/docs")
sql_do = db.session
