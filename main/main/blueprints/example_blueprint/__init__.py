from ...builtins.functions.import_mgr import load_config
from flask import Blueprint
from os import path

config = load_config(from_file_dir=path.dirname(path.realpath(__file__)))
bp = Blueprint(**config['settings'], **config['blueprint'])
