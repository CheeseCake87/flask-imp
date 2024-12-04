import re
import typing as t

import click


def strip_leading_slash(url_prefix: str) -> str:
    if url_prefix.startswith("/"):
        return url_prefix[1:]
    return url_prefix


def to_snake_case(string: str) -> str:
    """
    Thank you openai
    """
    # Replace any non-alphanumeric characters with underscores
    string = re.sub(r"[^a-zA-Z0-9]", "_", string)
    # Remove any consecutive underscores
    string = re.sub(r"_{2,}", "_", string)
    # Convert the string to lowercase
    string = string.lower()
    return string


class Sprinkles:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def build(
    folders: t.Dict[str, t.Any], files: t.Dict[str, t.Any], building: str = "App"
) -> None:
    # write_bytes: t.List[str] = []

    for folder, path in folders.items():
        if not path.exists():
            path.mkdir(parents=True)
            click.echo(
                f"{Sprinkles.OKGREEN}{building} folder: {folder}, created{Sprinkles.END}"
            )
        else:
            click.echo(
                f"{Sprinkles.WARNING}{building} folder already exists: {folder}, skipping{Sprinkles.END}"
            )

    for file, (path, content) in files.items():
        if not path.exists():
            # write files in bytes (this was old code, keeping it for reference)
            # if file in write_bytes:
            #     path.write_bytes(bytes.fromhex(content))
            #     continue

            path.write_text(content, encoding="utf-8")

            click.echo(
                f"{Sprinkles.OKGREEN}{building} file: {file}, created{Sprinkles.END}"
            )
        else:
            click.echo(
                f"{Sprinkles.WARNING}{building} file already exists: {file}, skipping{Sprinkles.END}"
            )
