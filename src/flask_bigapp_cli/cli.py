import re
from pathlib import Path

import click

from .resources import Resources as CLIResources
from flask_bigapp.resources import Resources


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


@click.group()
def cli():
    pass  # Entry Point


@cli.command("add-blueprint", help="Create a flask-bigapp blueprint")
@click.option(
    '-f', '--folder',
    nargs=1,
    default="Current Working Directory",
    prompt=(f'\n{Sprinkles.WARNING}(Creation is relative to the current working directory){Sprinkles.END}\n'
            f'Folder to create blueprint in'),
    help='The from_folder to create the blueprint in, defaults to the current working directory'
)
@click.option(
    '-n', '--name',
    nargs=1,
    default="my_new_blueprint",
    prompt='Name of the blueprint to create',
    help='The name of the blueprint to create'
)
def add_blueprint(folder, name):
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

    # Prepare blueprint folders for loop creation
    folders = (bp_folder, bp_routes_folder, bp_templates_folder, bp_static_folder,)

    # Loop create folders
    for folder in folders:
        if not folder.exists():
            folder.mkdir(parents=True)
        else:
            click.echo(f"{Sprinkles.WARNING}Folder already exists: {folder}, skipping{Sprinkles.END}")

    # Create __init__.py
    if not bp_init.exists():
        bp_init.write_text(CLIResources.blueprint_init)
    else:
        click.echo(f"{Sprinkles.WARNING}__init__ already exists: {bp_init}, skipping{Sprinkles.END}")

    # Create config.toml
    if not bp_config.exists():
        bp_config.write_text(
            CLIResources.blueprint_config.format(
                name=name
            )
        )
    else:
        click.echo(f"{Sprinkles.WARNING}Config already exists: {bp_config}, skipping{Sprinkles.END}")

    # Create blueprint index.py route
    if not bp_route.exists():
        bp_route.write_text(CLIResources.blueprint_index_route)
    else:
        click.echo(f"{Sprinkles.WARNING}Route already exists: {bp_route}, skipping{Sprinkles.END}")

    # Create blueprint index.html template
    if not bp_template.exists():
        bp_template.write_text(CLIResources.blueprint_index_template.format(name=name))
    else:
        click.echo(f"{Sprinkles.WARNING}Template already exists: {bp_template}, skipping{Sprinkles.END}")

    click.echo(f"{Sprinkles.OKGREEN}Blueprint created: {bp_folder}{Sprinkles.END}")


@cli.command("init", help="Create a global collection folder")
def create_global_collection():
    cwd = Path.cwd()

    app_folder = cwd / "app"

    gc_folder = app_folder / "global"

    tlf = (
        "routes",
        "templates",
        "static",
        "context_processors",
        "error_handlers",
        "filters",
    )

    static_folders = (
        "css",
        "js",
        "img",
    )

    templates_folders = (
        "errors",
        "extends",
        "includes",
    )

    tlf_lookup = dict()

    # Prepare global folder structure
    for folder in tlf:
        tlf_lookup[folder] = gc_folder / folder
        this_folder = gc_folder / folder
        if not this_folder.exists():
            this_folder.mkdir(parents=True)

    # Prepare static folders
    for folder in static_folders:
        this_folder = gc_folder / "static" / folder
        if not this_folder.exists():
            this_folder.mkdir(parents=True)

    # Prepare templates folders
    for folder in templates_folders:
        this_folder = gc_folder / "templates" / folder
        if not this_folder.exists():
            this_folder.mkdir(parents=True)

    file_lu = {
        "context_processors.py": (
            tlf_lookup["context_processors"] / "context_processors.py",
            CLIResources.global_context_processors_py
        ),
        "error_handlers.py": (
            tlf_lookup["error_handlers"] / "error_handlers.py",
            CLIResources.global_error_handlers_py
        ),
        "filters.py": (
            tlf_lookup["filters"] / "filters.py",
            CLIResources.global_filters_py
        ),
        "routes.py": (
            tlf_lookup["routes"] / "routes.py",
            CLIResources.global_routes_py
        ),
        "main.css": (
            tlf_lookup["static"] / "css" / "main.css",
            CLIResources.global_static_main_css
        ),
        "main.js": (
            tlf_lookup["static"] / "js" / "main.js",
            CLIResources.global_static_main_js
        ),
        "Flask-BigApp-Logo.svg": (
            tlf_lookup["static"] / "img" / "Flask-BigApp-Logo.svg",
            CLIResources.global_static_logo_svg
        ),
        "index.html": (
            tlf_lookup["templates"] / "index.html",
            CLIResources.index_html
        ),
        "400.html": (
            tlf_lookup["templates"] / "errors" / "400.html",
            CLIResources.page_400
        ),
        "401.html": (
            tlf_lookup["templates"] / "errors" / "401.html",
            CLIResources.page_401
        ),
        "403.html": (
            tlf_lookup["templates"] / "errors" / "403.html",
            CLIResources.page_403
        ),
        "404.html": (
            tlf_lookup["templates"] / "errors" / "404.html",
            CLIResources.page_404
        ),
        "405.html": (
            tlf_lookup["templates"] / "errors" / "405.html",
            CLIResources.page_405
        ),
        "500.html": (
            tlf_lookup["templates"] / "errors" / "500.html",
            CLIResources.page_500
        ),
        "main.html": (
            tlf_lookup["templates"] / "extends" / "main.html",
            CLIResources.extends_main
        ),
        "footer.html": (
            tlf_lookup["templates"] / "includes" / "footer.html",
            CLIResources.includes_footer
        ),
        "header.html": (
            tlf_lookup["templates"] / "includes" / "header.html",
            CLIResources.includes_header
        ),
    }

    # Prepare global files
    for file, res in file_lu.items():
        if not res(0).exists():
            res(0).write_text(res(1))
        else:
            click.echo(f"{Sprinkles.WARNING}File already exists: {res(0)}, skipping{Sprinkles.END}")
