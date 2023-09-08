import re


def to_snake_case(string):
    """
    Thank you openai
    """
    # Replace any non-alphanumeric characters with underscores
    string = re.sub(r'[^a-zA-Z0-9]', '_', string)
    # Remove any consecutive underscores
    string = re.sub(r'_{2,}', '_', string)
    # Convert the string to lowercase
    string = string.lower()
    return string


class Sprinkles:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
