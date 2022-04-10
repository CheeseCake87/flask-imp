from .utilities import find_illegal_dir_char
from .utilities import show_stats
from .utilities import get_app_root
from configparser import ConfigParser
from os import path, listdir

app_root = get_app_root()


def load_modules(module_folder: str) -> list:
    """
    takes in a module folder name, reads the config of module, if enabled and no errors adds the name to the list
    to import.
    :param module_folder:
    :return list[enabled & valid module names]:
    """
    if module_folder[-1:] == "s":
        deco_dir_name = module_folder[:-1].upper()
    else:
        deco_dir_name = module_folder.upper()
    modules = []
    for module in find_modules(module_folder=module_folder):
        # passes config file find to load_import_config
        module_config = load_config(module_folder=module_folder, module=module)
        if "error" in module_config:
            show_stats(f":| ERROR LOADING CONFIG FOR [{module}] |:")
            continue

        config_type = module_config['init']['type']
        version = module_config['init']['version']
        enabled = module_config['init']['enabled']

        if config_type != deco_dir_name.lower():
            show_stats(f":| YOU HAVE NON {deco_dir_name} MODULE TYPE IN THE {module_folder} FOLDER |:")
            continue

        if enabled == "no":
            show_stats(f":| {deco_dir_name} DISABLED [{module}] v{version} |:")
            continue
        show_stats(" ")
        show_stats(f":| {deco_dir_name} FOUND [{module}] v{version} |:")
        modules.append(module)

    return modules


def find_modules(module_folder: str) -> list:
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
            show_stats(f":! ERROR when importing [{item}]: Illegal dir char found !:")
            continue

        if path.isdir(f"{app_root}/{module_folder}/{item}"):
            dir_clean.append(item)

    return dir_clean


def import_routes(module_folder: str = None, module: str = None) -> list:
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


def load_config(module_folder: str = None, module: str = None, from_file_dir: str = None,
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
                    if inner_value == "True" or inner_value == "true" or inner_value == "yes":
                        loop_dict[inner_key] = True
                        continue
                    if inner_value == "False" or inner_value == "false" or inner_value == "no":
                        loop_dict[inner_key] = False
                        continue
                    try:
                        loop_dict[inner_key] = int(inner_value)
                        continue
                    except ValueError:
                        loop_dict[inner_key] = inner_value
                doctored_settings[key] = loop_dict

            doctored_settings["app"]["root"] = get_app_root()
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
