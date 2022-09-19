from datetime import datetime, timedelta
from distutils import util
from os import mkdir
from os import path
from os import remove
from re import sub
from shutil import rmtree

from pytz import timezone


def remove_escapes(string: str, remove_these: list = None) -> str:
    """
    Used to remove escapes like \n and \t in a string value.
    Takes in a list of predefined removables, can add more if needed.
    See [if remove is none] in code to see available removables.
    :param string:
    :param remove_these:
    :return:
    """
    if remove_these is None:
        remove_these = ['new_line', 'tab', 'dead_space']
    if "tab" in remove_these:
        string = sub(r'^[ \t]+|[ \t]', ' ', string)
    if "new_line" in remove_these:
        string = sub(r'^[ \n]+|[ \n]', ' ', string)
    if "dead_space" in remove_these:
        string = sub(r' +', ' ', string)
    return string


def find_illegal_char(name: str) -> bool:
    """
    This finds characters that are not allowed in the specified name var
    :param name:
    :return bool:
    """
    illegal_characters = ['%', '$', '£', ' ', '#']
    for char in illegal_characters:
        if char in name:
            return True
    return False


def regular_datetime(ltz: str = "Europe/London", days_delta: int = 0) -> datetime:
    """
    Returns the current date and time YYYY-MM-DD HH:MM:SS for the defined local time zone,
    can also adjust the date by using a delta(days)
    :param days_delta:
    :param ltz:
    :return:
    """
    local_tz = timezone(ltz)
    if days_delta < 0:
        apply_delta = (datetime.now(local_tz) - timedelta(days=days_delta)).strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(apply_delta, "%Y-%m-%d %H:%M:%S")
    if days_delta > 0:
        apply_delta = (datetime.now(local_tz) + timedelta(days=days_delta)).strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(apply_delta, "%Y-%m-%d %H:%M:%S")
    return datetime.strptime(datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")


def regular_date(ltz: str = "Europe/London", days_delta: int = 0) -> datetime:
    """
    Returns the current date YYYY-MM-DD for the defined local time zone,
    can also adjust the date by using a delta(days)
    :param days_delta:
    :param ltz:
    :return:
    """
    local_tz = timezone(ltz)
    if days_delta < 0:
        apply_delta = (datetime.now(local_tz) - timedelta(days=days_delta)).strftime("%Y-%m-%d")
        return datetime.strptime(apply_delta, "%Y-%m-%d")
    if days_delta > 0:
        apply_delta = (datetime.now(local_tz) + timedelta(days=days_delta)).strftime("%Y-%m-%d")
        return datetime.strptime(apply_delta, "%Y-%m-%d")
    return datetime.strptime(datetime.now(local_tz).strftime("%Y-%m-%d"), "%Y-%m-%d")


def regular_datetime_string(ltz: str = "Europe/London", days_delta: int = 0) -> str:
    """
    Returns date YEAR-MONTH-DAY HOUR:MIN:SEC in string
    Able to take day delta, minus days passed in as negative
    example: delta=-20 for minus 20 days
    :param ltz:
    :param days_delta:
    :return str:
    """
    local_tz = timezone(ltz)
    if days_delta < 0:
        return (datetime.now(local_tz) - timedelta(days=days_delta)).strftime("%Y-%m-%d %H:%M:%S")
    if days_delta > 0:
        return (datetime.now(local_tz) + timedelta(days=days_delta)).strftime("%Y-%m-%d %H:%M:%S")
    return (datetime.now(local_tz)).strftime("%Y-%m-%d %H:%M:%S")


def regular_date_string(ltz: str = "Europe/London", days_delta: int = 0) -> str:
    """
    Returns date YEAR-MONTH-DAY in string
    Able to take day delta, minus days passed in as negative
    example: delta=-20 for minus 20 days
    :param ltz:
    :param days_delta:
    :return str:
    """
    local_tz = timezone(ltz)
    if days_delta < 0:
        return (datetime.now(local_tz) - timedelta(days=days_delta)).strftime("%Y-%m-%d")
    if days_delta > 0:
        return (datetime.now(local_tz) + timedelta(days=days_delta)).strftime("%Y-%m-%d")
    return (datetime.now(local_tz)).strftime("%Y-%m-%d")


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


def get_file_extension(file_path: str) -> str:
    """
    Gets the file extension from file_path
    """
    return path.splitext(file_path)[1]


def get_filename_without_extension(file_path: str) -> str:
    """
    Gets filename from file_path without extension
    """
    return path.splitext(path.basename(file_path))[0]


def get_filename_with_extension(file_path: str) -> str:
    """
    Gets filename from file_path
    """
    return path.basename(file_path)


def make_filename_safe(file_path: str):
    """
    Replaces non-alpha-numeric characters with _
    """
    safe_filename = sub(r"\W+", "_", get_filename_without_extension(file_path))
    return f"{safe_filename}{get_file_extension(file_path)}"


def create_folder_if_not_found(folder_path: str) -> str:
    """
    Checks if folder_path exists, if not creates it.
    """
    if path.exists(folder_path):
        return folder_path
    try:
        mkdir(folder_path)
    except OSError:
        return "none"
    return folder_path


def path_exists(folder_path: str) -> bool:
    """
    Checks if folder_path exists
    """
    if path.exists(folder_path):
        return True
    return False


def delete_file(file_path: str) -> bool:
    """
    Checks if file_path is a file, if true deletes it. If not, ignores and returns false.
    """
    if path.isfile(file_path):
        remove(file_path)
        return True
    return False


def delete_folder(folder_path: str) -> bool:
    """
    Checks if folder_path is a dir, if true deletes it. If not, ignores and returns false.
    """
    if path.isdir(folder_path):
        rmtree(folder_path)
        return True
    return False


def is_file(file_path: str) -> bool:
    """
    Returns true is file_path is a file
    """
    if path.isfile(file_path):
        return True
    return False


def is_dir(dir_path: str) -> bool:
    """
    Returns true is dir_path is a dir
    """
    if path.isdir(dir_path):
        return True
    return False


def string_to_bool(bool_str: str) -> bool:
    """
    Converts a string value to a bool value
    """
    return bool(util.strtobool(bool_str))


def is_string_bool(bool_str: str) -> bool:
    """
    Checks if a string value can be seen as a book (yes, true, 1)
    """
    try:
        v = util.strtobool(bool_str)
        if isinstance(v, int):
            return True
    except ValueError:
        return False


def reverse_dict(input_dict: dict) -> dict:
    """
    Swaps the values with keys of a dict
    """
    return_dict = {}
    for key, value in input_dict.items():
        return_dict[value] = key
    return return_dict
