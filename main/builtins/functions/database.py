from importlib import import_module
from inspect import getmembers
from inspect import isclass
from os import path
from sys import modules

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import ArgumentError
from sqlalchemy.exc import InvalidRequestError

from .utilities import get_app_root

db = SQLAlchemy()
sql_do = db.session
app_root = get_app_root()


def convert_sql_to_list_dict(query, return_only_these_fields: list = None) -> list:
    return_list = []
    for value in query:
        temp_dict = {}
        vars_dict = vars(value)
        for inner_key, inner_value in vars_dict.items():
            if isinstance(return_only_these_fields, list):
                if inner_key in return_only_these_fields:
                    temp_dict[inner_key] = inner_value
            else:
                temp_dict[inner_key] = inner_value
        return_list.append(temp_dict)
    return return_list


def convert_sql_to_dict(query, return_only_these_fields: list = None) -> dict:
    for value in query:
        temp_dict = {}
        vars_dict = vars(value)
        for inner_key, inner_value in vars_dict.items():
            if isinstance(return_only_these_fields, list):
                if inner_key in return_only_these_fields:
                    temp_dict[inner_key] = inner_value
            else:
                temp_dict[inner_key] = inner_value
        return temp_dict


def has_table(module, table_name: str) -> bool:
    """
    Takes in module name and the table(Class) name in the models.py file, attempts to query using the information and
    returns True if successful query, and False if not. Used to check if a table exists.
    :param module:
    :param table_name:
    :return:
    """
    if table_name == "ForeignKey":
        return False
    try:
        _import = import_module(f"{current_app.config['APP_NAME']}.blueprints.{module}.models")
    except ModuleNotFoundError:
        _import = import_module(f"{current_app.config['APP_NAME']}.extensions.{module}.models")

    _attr = getattr(_import, table_name)
    print(type(_attr))
    try:
        sql_do.query(_attr).all()
        return True
    except (OperationalError, ArgumentError, InvalidRequestError):
        return False





def get_tables() -> dict:
    """
    Returns a dict of modules that have model.py files, the classes within, and if the table exists in the database.
    dict shape: {module_name: [ (class_name, exists_in_database_bool), (class_name, exists_in_database_bool)] }
    dict, list of tuples
    :return dict:
    """
    models = {}
    print(current_app.config["SHARED_MODELS"])
    for key, value in current_app.config["SHARED_MODELS"].items():
        if key not in models:
            models[key] = []

        try:
            mod = getmembers(
                modules[f"{current_app.config['APP_NAME']}.blueprints.{key}.models"], isclass
            )
            for m in mod:
                class_name = m[0]
                if class_name_ok(class_name):
                    models[key].append((class_name, has_table(module=key, table_name=class_name)))
        except KeyError:
            mod = getmembers(
                modules[f"{current_app.config['APP_NAME']}.extensions.{key}.models"], isclass
            )
            for m in mod:
                class_name = m[0]
                if class_name_ok(class_name):
                    models[key].append((class_name, has_table(module=key, table_name=class_name)))

    return models


def find_model_location(module_name: str) -> str:
    """
    Takes in module name, checks in the module folder if a models.py file exists then returns the correct import path.
    :param module_name:
    :return:
    """
    if path.isfile(f"{app_root}/api/{module_name}/models/models.py"):
        return f"{current_app.config['APP_NAME']}.api.{module_name}.models.models"
    if path.isfile(f"{app_root}/blueprints/{module_name}/models/models.py"):
        return f"{current_app.config['APP_NAME']}.blueprints.{module_name}.models.models"
    if path.isfile(f"{app_root}/extensions/{module_name}/models/models.py"):
        return f"{current_app.config['APP_NAME']}.extensions.{module_name}.models.models"
    return ""
