from os import listdir
from os import path
from json import load

from .utilities import find_illegal_dir_char
from .utilities import get_app_root
from .utilities import show_stats
from .utilities import is_string_bool
from .utilities import string_to_bool

app_root = get_app_root()


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


def load_modules(module_folder: str, builtin: bool = False) -> list:
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
    for module in find_modules(module_folder=module_folder):
        # passes config file find to load_import_config
        module_config = read_config_as_dict(module_folder=module_folder, module=module)
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


def read_nav(nav_path: str) -> dict:
    with open(nav_path, "r") as nav:
        loaded_nav = load(nav)
    return loaded_nav
