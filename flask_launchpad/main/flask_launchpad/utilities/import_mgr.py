from configparser import ConfigParser
from os import listdir
from os import path
from json import load
from distutils import util


def find_illegal_dir_char(name: str) -> bool:
    """
    For use in directory actions, this finds characters that are
    not allowed to be used when importing from directories
    :param name:
    :return bool:
    """
    illegal_characters = ['%', '$', '£', ' ', '#']
    for char in illegal_characters:
        if char in name:
            return True
    return False


def is_string_bool(bool_str: str) -> bool:
    try:
        v = util.strtobool(bool_str)
        if isinstance(v, int):
            return True
    except ValueError:
        return False


def string_to_bool(bool_str: str) -> bool:
    return bool(util.strtobool(bool_str))


def find_modules(app_root: str, module_folder: str) -> list:
    """
    Scans the passed in modules folder for module directories,
    uses listdir - removes cache folders, removes files

    :return list[module folders]:
    """

    dir_raw, dir_clean = listdir(f"{app_root}/{module_folder}/"), []

    for item in dir_raw:
        if "__" in item:
            continue

        if find_illegal_dir_char(item):
            continue

        if path.isdir(f"{app_root}/{module_folder}/{item}"):
            dir_clean.append(item)

    return dir_clean


def load_modules(app_root: str, module_folder: str, builtin: bool = False) -> list:
    """
    takes in a module folder name, reads the config of module, if enabled and no errors adds the name to the list
    to import.
    :param module_folder:
    :param builtin:
    :return list[enabled & valid module names]:
    """
    if module_folder[-1:] == "s":
        deco_dir_name = module_folder[:-1].upper()
    else:
        deco_dir_name = module_folder.upper()

    if builtin:
        module_folder = f"builtins/{module_folder}"

    modules = []
    for module in find_modules(app_root, module_folder=module_folder):
        # passes config file find to load_import_config
        module_config = read_config_as_dict(app_root, module_folder=module_folder, module=module)
        if "error" in module_config:
            continue

        config_type = module_config['init']['type']
        version = module_config['init']['version']
        enabled = module_config['init']['enabled']

        if config_type != deco_dir_name.lower():
            continue

        if enabled == "no":
            continue

        modules.append(module)

    return modules


def import_routes(app_root: str, module_folder: str = None, module: str = None) -> list:
    """
    Uses listdir to get all routes in module list, removing dunder, readme and files with characters that are deemed
    illegal.
    :return list[valid routes]:
    """
    deco_dir_name = module_folder[:-1].upper()
    routes_raw, routes_clean, display_module = "", [], ""

    if module_folder == "builtins":
        routes_raw = listdir(f"{app_root}/{module_folder}/{module}")
    else:
        routes_raw = listdir(f"{app_root}/{module_folder}/{module}/routes")

    for item in routes_raw:
        if "__" in item:
            continue

        if "readme" in item:
            continue

        if find_illegal_dir_char(item):
            print(f":! {deco_dir_name} : ERROR in [{module}] route [{item}]: Illegal char found !:")
            continue

        if not item.endswith(".py"):
            print(f":! {deco_dir_name} : ERROR in [{module}] route [{item}]: Illegal file found !:")
            continue

        routes_clean.append(item.replace(".py", ""))

    return routes_clean


def read_config_as_dict(app_root: str, module_folder: str = None, module: str = None, from_file_dir: str = None,
                        app_config: bool = False, api_config: bool = False) -> dict:
    """
    Takes in the current working directory of the import, then returns
    the config file values in its directory as a dict
    :param app_config:
    :param api_config:
    :param module_folder:
    :param module:
    :param from_file_dir:
    :return dict[error: bool / config file]:
    """
    if app_config:
        if path.isfile(f"{app_root}/app_config.ini"):
            config = ConfigParser()
            config.read(f"{app_root}/app_config.ini")
            config_to_dict = config.__dict__['_sections']
            doctored_settings = {}
            for key, value in config_to_dict.items():
                loop_dict = {}
                for inner_key, inner_value in value.items():
                    if is_string_bool(inner_value):
                        loop_dict[inner_key] = string_to_bool(inner_value)
                        continue
                    try:
                        loop_dict[inner_key] = int(inner_value)
                        continue
                    except ValueError:
                        loop_dict[inner_key] = inner_value
                doctored_settings[key] = loop_dict

            doctored_settings["app"]["root"] = app_root
            return doctored_settings

    if api_config:
        if path.isfile(f"{app_root}/api/config.ini"):
            config = ConfigParser()
            config.read(f"{app_root}/api/config.ini")
            config_to_dict = config.__dict__['_sections']
            return config_to_dict

    if from_file_dir is not None:
        if path.isfile(f"{from_file_dir}/config.ini"):
            config = ConfigParser()
            config.read(f"{from_file_dir}/config.ini")
            config_to_dict = config.__dict__['_sections']
            return config_to_dict

    if path.isfile(f"{app_root}/{module_folder}/{module}/config.ini"):
        config = ConfigParser()
        config.read(f"{app_root}/{module_folder}/{module}/config.ini")
        config_to_dict = config.__dict__['_sections']
        return config_to_dict

    return {"error": True}


def read_app_config(app_root: str, section: str = None):
    config = ConfigParser()
    config.read(f"{app_root}/app_config.ini")
    if section is not None:
        return config[section]
    return config


def read_config(app_root: str, module: str = None, filepath: str = None, section: str = None):
    """
    Finds the config file for the passed in module.
    :param module:
    :param filepath:
    :param section:
    :return dict:
    """
    config = ConfigParser()
    if module is not None:
        if path.isfile(f"{app_root}/api/{module}/config.ini"):
            config.read(f"{app_root}/api/{module}/config.ini")
            if section is not None:
                return config[section]
            return config
        if path.isfile(f"{app_root}/blueprints/{module}/config.ini"):
            config.read(f"{app_root}/blueprints/{module}/config.ini")
            if section is not None:
                return config[section]
            return config
        if path.isfile(f"{app_root}/extensions/{module}/config.ini"):
            config.read(f"{app_root}/extensions/{module}/config.ini")
            if section is not None:
                return config[section]
            return config

    if filepath is not None:
        if path.isfile(f"{filepath}/config.ini"):
            config.read(f"{filepath}/config.ini")
            if section is not None:
                return config[section]
            return config

    raise FileNotFoundError


def read_nav(nav_path: str) -> dict:
    with open(nav_path, "r") as nav:
        loaded_nav = load(nav)
    return loaded_nav
