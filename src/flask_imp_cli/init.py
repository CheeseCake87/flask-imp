import os
from pathlib import Path

import click

from .blueprint import add_blueprint
from .filelib.all_files import GlobalFileLib
from .filelib.favicon import favicon
from .filelib.app import AppFileLib
from .helpers import Sprinkles as Sp


def init_app(name):
    click.echo(f"{Sp.OKGREEN}Creating App: {name}")

    cwd = Path.cwd()

    app_folder = cwd / name

    if app_folder.exists():
        click.echo(f"{Sp.FAIL}{name} folder already exists!{Sp.END}")
        click.confirm("Are you sure you want to continue?", abort=True)

    # Folders
    folders = {
        "root": app_folder,
        "models": app_folder / "models",
        "blueprints": app_folder / "blueprints",
        "extensions": app_folder / "extensions",
        "global": app_folder / "global",
        "global/cli": app_folder / "global" / "cli",
        "global/context_processors": app_folder / "global" / "context_processors",
        "global/error_handlers": app_folder / "global" / "error_handlers",
        "global/filters": app_folder / "global" / "filters",
        "global/routes": app_folder / "global" / "routes",
        "global/static": app_folder / "global" / "static",
        "global/templates": app_folder / "global" / "templates",
        "global/templates/errors": app_folder / "global" / "templates" / "errors",
    }

    # Files
    files = {
        "root/default.config.toml": (
            folders['root'] / "default.config.toml",
            AppFileLib.default_init_config_toml.format(secret_key=os.urandom(24).hex())
        ),
        "root/__init__.py": (
            folders['root'] / "__init__.py",
            AppFileLib.init_py.format(app_name=name)
        ),
        "models/__init__.py": (
            folders['models'] / "__init__.py",
            AppFileLib.models_init_py.format(app_name=name)
        ),
        "models/example_user_table.py": (
            folders['models'] / "example_user_table.py",
            AppFileLib.models_example_user_table_py
        ),
        "extensions/__init__.py": (
            folders['extensions'] / "__init__.py",
            AppFileLib.extensions_init_py
        ),
        "global/cli/cli.py": (
            folders['global/cli'] / "cli.py",
            GlobalFileLib.collections_cli_py.format(app_name=name)
        ),
        "global/context_processors/context_processors.py": (
            folders['global/context_processors'] / "context_processors.py",
            GlobalFileLib.collections_context_processors_py
        ),
        "global/error_handlers/error_handlers.py": (
            folders['global/error_handlers'] / "error_handlers.py",
            GlobalFileLib.collections_error_handlers_py
        ),
        "global/filters/filters.py": (
            folders['global/filters'] / "filters.py",
            GlobalFileLib.collections_filters_py
        ),
        "global/routes/routes.py": (
            folders['global/routes'] / "routes.py",
            GlobalFileLib.collections_routes_py
        ),
        "global/static/favicon.ico": (
            folders['global/static'] / "favicon.ico",
            favicon,
        ),
        "global/templates/index.html": (
            folders['global/templates'] / "index.html",
            GlobalFileLib.templates_index_html
        ),
        "global/templates/errors/400.html": (
            folders['global/templates/errors'] / "400.html",
            GlobalFileLib.templates_errors_400_html
        ),
        "global/templates/errors/401.html": (
            folders['global/templates/errors'] / "401.html",
            GlobalFileLib.templates_errors_401_html
        ),
        "global/templates/errors/403.html": (
            folders['global/templates/errors'] / "403.html",
            GlobalFileLib.templates_errors_403_html
        ),
        "global/templates/errors/404.html": (
            folders['global/templates/errors'] / "404.html",
            GlobalFileLib.templates_errors_404_html
        ),
        "global/templates/errors/405.html": (
            folders['global/templates/errors'] / "405.html",
            GlobalFileLib.templates_errors_405_html
        ),
        "global/templates/errors/500.html": (
            folders['global/templates/errors'] / "500.html",
            GlobalFileLib.templates_errors_500_html
        ),
    }

    # Loop create folders
    for folder, path in folders.items():
        if not path.exists():
            path.mkdir(parents=True)
            click.echo(f"{Sp.OKGREEN}App folder: {folder}, created{Sp.END}")
        else:
            click.echo(f"{Sp.WARNING}App folder already exists: {folder}, skipping{Sp.END}")

    # Loop create files
    for file, (path, content) in files.items():
        if not path.exists():

            if file == "global/static/favicon.ico":
                path.write_bytes(bytes.fromhex(content))
                continue

            path.write_text(content, encoding="utf-8")

            click.echo(f"{Sp.OKGREEN}App file: {file}, created{Sp.END}")
        else:
            click.echo(f"{Sp.WARNING}App file already exists: {file}, skipping{Sp.END}")

    add_blueprint(f"{name}/blueprints", "www", _init_app=True, _cwd=folders['blueprints'])

    click.echo(" ")
    click.echo(f"{Sp.OKBLUE}==================={Sp.END}")
    click.echo(f"{Sp.OKBLUE}Flask app deployed!{Sp.END}")
    click.echo(f"{Sp.OKBLUE}==================={Sp.END}")
    click.echo(" ")
    click.echo(f"{Sp.OKGREEN}'/' route is set by the blueprint named www{Sp.END}")
    click.echo(f"{Sp.OKGREEN}found in the blueprints folder. It is encouraged{Sp.END}")
    click.echo(f"{Sp.OKGREEN}to use blueprints to set all app routes.{Sp.END}")
    click.echo(" ")
    click.echo(f"{Sp.OKGREEN}All app (non-blueprint) resources can be found{Sp.END}")
    click.echo(f"{Sp.OKGREEN}in the global folder. Have a look through this{Sp.END}")
    click.echo(f"{Sp.OKGREEN}folder to find out more.{Sp.END}")
    click.echo(" ")
    if name == 'app':
        click.echo(f"{Sp.OKBLUE}Your app has the default name of 'app'{Sp.END}")
        click.echo(f"{Sp.OKBLUE}Flask will automatically look for this!{Sp.END}")
        click.echo(f"{Sp.OKBLUE}Run: flask run --debug{Sp.END}")
    else:
        click.echo(f"{Sp.OKBLUE}Your app has the name of '{name}'{Sp.END}")
        click.echo(f"{Sp.OKBLUE}Run: flask --app {name} run --debug{Sp.END}")
