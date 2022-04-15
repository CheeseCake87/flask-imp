from datetime import datetime, timedelta
from pytz import timezone
from json import load, dumps
from os import path
from os import mkdir
from os import remove
from re import sub
from flask import session
import emoji


def get_app_root() -> str:
    """
    Finds the root folder of the app.
    :return str: /app/folder/extend
    """
    strip = path.dirname(path.realpath(__file__)).split("/")[1:-2]
    return "/" + "/".join(strip)


def show_stats(print_this: str, enabled: bool = True) -> None:
    """
    used as a terminal display tool to output status.
    :param print_this:
    :param enabled:
    :return None:
    """
    if enabled:
        print(print_this)


def clear_error() -> None:
    session["error"] = None


def clear_message() -> None:
    session["message"] = None


def building_rocket() -> str:
    return emoji.emojize("""
>>>> BUILDING ROCKET :factory:""")


def rocket_launched() -> str:
    return emoji.emojize("""
>>>> ROCKET LAUNCHED :rocket:""")


def email_server_status(status: bool) -> str:
    if status:
        return emoji.emojize(f"""
>>>> EMAIL SERVER ENABLED :e-mail: :blue_circle:""")

    return emoji.emojize(f"""
>>>> EMAIL SERVER DISABLED :e-mail: :red_circle:""")


def sqlite_detected() -> str:
    return emoji.emojize(f"""
>>>> SQLITE TYPE DETECTED :information:
>> VISIT http://127.0.0.1:5000/reset-sqlite TO DROP AND RECREATE THE DATABASE
>> """)


def remove_escapes(string: str, remove: list = None) -> str:
    """
    Used to remove escapes like \n and \t in a string value.
    Takes in a list of predefined removables, can add more if needed.
    See [if remove is none] in code to see available removables.
    :param string:
    :param remove:
    :return:
    """
    if remove is None:
        remove = ['new_line', 'tab', 'dead_space']
    if "tab" in remove:
        string = sub(r'^[ \t]+|[ \t]', ' ', string)
    if "new_line" in remove:
        string = sub(r'^[ \n]+|[ \n]', ' ', string)
    if "dead_space" in remove:
        string = sub(r' +', ' ', string)
    return string


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


def regular_datetime(delta: int = 0) -> datetime:
    local_timestamp = timezone("Europe/London")
    if delta < 0:
        apply_delta = (datetime.now(local_timestamp) - timedelta(days=delta)).strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(apply_delta, "%Y-%m-%d %H:%M:%S")
    if delta > 0:
        apply_delta = (datetime.now(local_timestamp) + timedelta(days=delta)).strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(apply_delta, "%Y-%m-%d %H:%M:%S")
    return datetime.strptime(datetime.now(local_timestamp).strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")


def regular_date(delta: int = 0) -> datetime:
    local_timestamp = timezone("Europe/London")
    if delta < 0:
        apply_delta = (datetime.now(local_timestamp) - timedelta(days=delta)).strftime("%Y-%m-%d")
        return datetime.strptime(apply_delta, "%Y-%m-%d")
    if delta > 0:
        apply_delta = (datetime.now(local_timestamp) + timedelta(days=delta)).strftime("%Y-%m-%d")
        return datetime.strptime(apply_delta, "%Y-%m-%d")
    return datetime.strptime(datetime.now(local_timestamp).strftime("%Y-%m-%d"), "%Y-%m-%d")


def regular_datetime_string(delta: int = 0) -> str:
    """
    Returns date YEAR-MONTH-DAY HOUR:MIN:SEC in string
    Able to take day delta, minus days passed in as negative
    example: delta=-20 for minus 20 days
    :param delta:
    :return str:
    """
    local_timestamp = timezone("Europe/London")
    if delta < 0:
        return (datetime.now(local_timestamp) - timedelta(days=-delta)).strftime("%Y-%m-%d %H:%M:%S")
    if delta > 0:
        return (datetime.now(local_timestamp) + timedelta(days=delta)).strftime("%Y-%m-%d %H:%M:%S")
    return (datetime.now(local_timestamp)).strftime("%Y-%m-%d %H:%M:%S")


def regular_date_string(delta: int = 0) -> str:
    """
    Returns date YEAR-MONTH-DAY in string
    Able to take day delta, minus days passed in as negative
    example: delta=-20 for minus 20 days
    :param delta:
    :return str:
    """
    local_timestamp = timezone("Europe/London")
    if delta < 0:
        return (datetime.now(local_timestamp) - timedelta(days=-delta)).strftime("%Y-%m-%d")
    if delta > 0:
        return (datetime.now(local_timestamp) + timedelta(days=delta)).strftime("%Y-%m-%d")
    return (datetime.now(local_timestamp)).strftime("%Y-%m-%d")


def write_log(function: str = "Not specified", out: str = "-", err: str = "-") -> None:
    """
    Writes log in JSON, creates file if file is not found
    :param function:
    :param out:
    :param err:
    :return None:
    """
    log_file = f"{get_app_root()}/logs/log.json"
    if not path.exists(log_file):
        with open(log_file, mode="w") as create_log_file:
            create_log_file.write(dumps({'log': []}, indent=2))
    current_log = {
        "date_added": regular_datetime_string(),
        "function": function,
        "out": out,
        "err": err
    }
    with open(log_file, mode="r") as load_log:
        log = load(load_log)

    log["log"].append(current_log)
    with open(log_file, mode="w") as append_log:
        append_log.write(dumps(log, indent=2))


def read_log() -> dict:
    """
    Reads log, returns dict
    :return dict:
    """
    log_file = f"{get_app_root()}/logs/log.json"
    if not path.exists(log_file):
        return {'log': []}

    with open(log_file, mode="r") as load_log:
        return load(load_log)


def url_var(string: str) -> str:
    """
    Slugs string then returns the string in a standard URL var of r
    :param string:
    :return str:
    """
    replace = [" ", ".", ":", "?"]
    for char in replace:
        string = string.replace(char, "-")
    return f"?r={string.lower()}"


def get_file_extension(file: str) -> str:
    return file.rsplit('.', 1)[1].lower()


def get_filename_without_extension(file: str) -> str:
    return path.basename(file).rsplit('.', 1)[0].lower()


def get_filename_with_extension(file: str) -> str:
    return path.basename(file)


def make_filename_safe(file: str):
    safe_filename = sub('\W+', '_', get_filename_without_extension(file))
    return f"{safe_filename}.{get_file_extension(file)}"


def create_folder_if_not_found(folder_path: str) -> str:
    if path.exists(folder_path):
        return folder_path
    try:
        mkdir(folder_path)
    except OSError:
        return "none"
    return folder_path


def path_exists(folder_path: str) -> bool:
    if path.exists(folder_path):
        return True
    return False


def delete_file(file_path: str) -> bool:
    if path.isfile(file_path):
        remove(file_path)
    return True


def is_file(file_path: str) -> bool:
    if path.isfile(file_path):
        return True
    return False


def is_dir(dir_path: str) -> bool:
    if path.isdir(dir_path):
        return True
    return False


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
