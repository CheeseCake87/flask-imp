import re
from pathlib import Path

import click

from .resources import Resources as CLIResources


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


def _add_blueprint(folder, name, _root=False):
    cwd = Path.cwd()
    if folder != "Current Working Directory":
        cwd = Path(cwd / folder)
    if not cwd.exists():
        click.echo(
            f"{Sprinkles.FAIL}{folder} does not exist.{Sprinkles.END}")
        return

    name = to_snake_case(name)

    # Prepare blueprint folder structure
    bp_folder = cwd / name
    bp_routes_folder = bp_folder / "routes"
    bp_templates_folder = bp_folder / "templates" / name
    bp_static_folder = bp_folder / "static"

    # Prepare blueprint files
    bp_init = bp_folder / "__init__.py"
    bp_config = bp_folder / "config.toml"
    bp_route = bp_routes_folder / "index.py"
    bp_template = bp_templates_folder / "index.html"
    bp_static_logo = bp_static_folder / "Flask-BigApp-Logo.svg"

    # Prepare blueprint folders for loop creation
    folders = (
        bp_folder,
        bp_routes_folder,
        bp_templates_folder,
        bp_static_folder,
    )

    # Loop create folders
    for folder in folders:
        if not folder.exists():
            folder.mkdir(parents=True)
            click.echo(f"{Sprinkles.OKGREEN}Blueprint folder: {folder.name}, created{Sprinkles.END}")
        else:
            click.echo(f"{Sprinkles.WARNING}Blueprint folder already exists: {folder.name}, skipping{Sprinkles.END}")

    # Create __init__.py
    if not bp_init.exists():
        bp_init.write_text(CLIResources.blueprint_init)
        click.echo(f"{Sprinkles.OKGREEN}Blueprint __init__ created{Sprinkles.END}")
    else:
        click.echo(f"{Sprinkles.WARNING}Blueprint __init__ already exists, skipping{Sprinkles.END}")

    # Create config.toml
    if not bp_config.exists():
        bp_config.write_text(
            CLIResources.blueprint_config.format(
                name=name,
                url_prefix=name if not _root else "",
            )
        )
        click.echo(f"{Sprinkles.OKGREEN}Blueprint config, created{Sprinkles.END}")
    else:
        click.echo(f"{Sprinkles.WARNING}Blueprint config already exists, skipping{Sprinkles.END}")

    # Create blueprint index.py route
    if not bp_route.exists():
        bp_route.write_text(CLIResources.blueprint_index_route)
        click.echo(f"{Sprinkles.OKGREEN}Blueprint route: {bp_route.name}, created{Sprinkles.END}")
    else:
        click.echo(f"{Sprinkles.WARNING}Blueprint route already exists: {bp_route.name}, skipping{Sprinkles.END}")

    # Create blueprint index.html template
    if not bp_template.exists():
        bp_template.write_text(CLIResources.blueprint_index_template.format(name=name))
        click.echo(f"{Sprinkles.OKGREEN}Blueprint template file: {bp_template.name}, created{Sprinkles.END}")
    else:
        click.echo(
            f"{Sprinkles.WARNING}Blueprint template file already exists: {bp_template.name}, skipping{Sprinkles.END}")

    # Create logo
    if not bp_static_logo.exists():
        bp_static_logo.write_text(CLIResources.global_static_logo_svg)
        click.echo(f"{Sprinkles.OKGREEN}Blueprint static image: {bp_static_logo.name}, created{Sprinkles.END}")
    else:
        click.echo(
            f"{Sprinkles.WARNING}Blueprint static image already exists: {bp_static_logo.name}, skipping{Sprinkles.END}")

    click.echo(f"{Sprinkles.OKGREEN}Blueprint created: {bp_folder}{Sprinkles.END}")
