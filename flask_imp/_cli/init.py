import os
from pathlib import Path

import click

from .blueprint import add_blueprint
from .filelib.all_files import GlobalFileLib
from .filelib.app import AppFileLib
from .filelib.favicon import favicon
from .filelib.flask_imp_logo import flask_imp_logo
from .filelib.head_tag_generator import head_tag_generator
from .filelib.water_css import water_css
from .helpers import Sprinkles as Sp


def init_app(name, _full: bool = False, _slim: bool = False, _minimal: bool = False):
    click.echo(f"{Sp.OKGREEN}Creating App: {name}")

    cwd = Path.cwd()

    app_folder = cwd / name

    if app_folder.exists():
        click.echo(f"{Sp.FAIL}{name} folder already exists!{Sp.END}")
        click.confirm("Are you sure you want to continue?", abort=True)

    # Folders
    folders = {
        "root": app_folder,
        "extensions": app_folder / "extensions",
        "global": app_folder / "global",
        "global/static": app_folder / "global" / "static",
        "global/templates": app_folder / "global" / "templates",
    }

    if _minimal:
        folders.update(
            {
                "global/static/css": app_folder / "global" / "static" / "css",
                "global/static/img": app_folder / "global" / "static" / "img",
            }
        )

    if not _minimal:
        folders.update(
            {
                "global/cli": app_folder / "global" / "cli",
                "global/error_handlers": app_folder / "global" / "error_handlers",
                "global/templates/errors": app_folder
                / "global"
                / "templates"
                / "errors",
            }
        )

    if not _slim:
        folders.update(
            {
                "models": app_folder / "models",
                "blueprints": app_folder / "blueprints",
                "global/context_processors": app_folder
                / "global"
                / "context_processors",
                "global/filters": app_folder / "global" / "filters",
                "global/routes": app_folder / "global" / "routes",
            }
        )

    # Files
    files = {
        "root/default.config.toml": (
            folders["root"] / "default.config.toml",
            AppFileLib.default_init_config_toml.format(secret_key=os.urandom(24).hex())
            if not _slim
            else AppFileLib.default_config_toml.format(secret_key=os.urandom(24).hex()),
        ),
        "root/__init__.py": (
            folders["root"] / "__init__.py",
            AppFileLib.init_py.format(app_name=name)
            if not _slim
            else AppFileLib.slim_init_py.format(app_name=name)
            if not _minimal
            else AppFileLib.minimal_init_py.format(app_name=name),
        ),
        "global/static/favicon.ico": (
            folders["global/static"] / "favicon.ico",
            favicon,
        ),
        "extensions/__init__.py": (
            folders["extensions"] / "__init__.py",
            AppFileLib.extensions_init_py
            if not _slim
            else AppFileLib.slim_extensions_init_py,
        ),
    }

    if _minimal:
        files.update(
            {
                "global/templates/index.html": (
                    folders["global/templates"] / "index.html",
                    GlobalFileLib.minimal_templates_index_html.format(
                        head_tag=head_tag_generator(
                            no_js=True,
                        ),
                        static_path="static",
                        index_py=folders["global"] / "index.py",
                        index_html=folders["global/templates"] / "index.html",
                        init_py=folders["root"] / "__init__.py",
                    ),
                ),
                "global/static/css/main.css": (
                    folders["global/static/css"] / "water.css",
                    water_css,
                ),
                "global/static/img/flask-imp-logo.png": (
                    folders["global/static/img"] / "flask-imp-logo.png",
                    flask_imp_logo,
                ),
                "global/routes.py": (
                    folders["global"] / "routes.py",
                    GlobalFileLib.minimal_collections_routes_py,
                ),
            }
        )

    if not _minimal:
        files.update(
            {
                "global/cli/cli.py": (
                    folders["global/cli"] / "cli.py",
                    GlobalFileLib.collections_cli_py.format(app_name=name)
                    if not _slim
                    else GlobalFileLib.slim_collections_cli_py,
                ),
                "global/error_handlers/error_handlers.py": (
                    folders["global/error_handlers"] / "error_handlers.py",
                    GlobalFileLib.collections_error_handlers_py,
                ),
                "global/templates/errors/400.html": (
                    folders["global/templates/errors"] / "400.html",
                    GlobalFileLib.templates_errors_400_html,
                ),
                "global/templates/errors/401.html": (
                    folders["global/templates/errors"] / "401.html",
                    GlobalFileLib.templates_errors_401_html,
                ),
                "global/templates/errors/403.html": (
                    folders["global/templates/errors"] / "403.html",
                    GlobalFileLib.templates_errors_403_html,
                ),
                "global/templates/errors/404.html": (
                    folders["global/templates/errors"] / "404.html",
                    GlobalFileLib.templates_errors_404_html,
                ),
                "global/templates/errors/405.html": (
                    folders["global/templates/errors"] / "405.html",
                    GlobalFileLib.templates_errors_405_html,
                ),
                "global/templates/errors/500.html": (
                    folders["global/templates/errors"] / "500.html",
                    GlobalFileLib.templates_errors_500_html,
                ),
            }
        )

    if not _slim:
        files.update(
            {
                "models/__init__.py": (
                    folders["models"] / "__init__.py",
                    AppFileLib.models_init_py.format(app_name=name),
                ),
                "models/example_user_table.py": (
                    folders["models"] / "example_user_table.py",
                    AppFileLib.models_example_user_table_py,
                ),
                "global/context_processors/context_processors.py": (
                    folders["global/context_processors"] / "context_processors.py",
                    GlobalFileLib.collections_context_processors_py,
                ),
                "global/filters/filters.py": (
                    folders["global/filters"] / "filters.py",
                    GlobalFileLib.collections_filters_py,
                ),
                "global/routes/routes.py": (
                    folders["global/routes"] / "routes.py",
                    GlobalFileLib.collections_routes_py,
                ),
                "global/templates/index.html": (
                    folders["global/templates"] / "index.html",
                    GlobalFileLib.templates_index_html,
                ),
            }
        )

    # Loop create folders
    for folder, path in folders.items():
        if not path.exists():
            path.mkdir(parents=True)
            click.echo(f"{Sp.OKGREEN}App folder: {folder}, created{Sp.END}")
        else:
            click.echo(
                f"{Sp.WARNING}App folder already exists: {folder}, skipping{Sp.END}"
            )

    # Loop create files
    for file, (path, content) in files.items():
        if not path.exists():
            if (
                file == "global/static/favicon.ico"
                or file == "global/static/img/flask-imp-logo.png"
            ):
                path.write_bytes(bytes.fromhex(content))
                continue

            path.write_text(content, encoding="utf-8")

            click.echo(f"{Sp.OKGREEN}App file: {file}, created{Sp.END}")
        else:
            click.echo(f"{Sp.WARNING}App file already exists: {file}, skipping{Sp.END}")

    if not _minimal:
        add_blueprint(
            f"{name}/blueprints",
            "www",
            _init_app=True,
            _cwd=folders["blueprints"] if not _slim else folders["root"],
        )

    click.echo(" ")
    click.echo(f"{Sp.OKBLUE}==================={Sp.END}")
    click.echo(f"{Sp.OKBLUE}Flask app deployed!{Sp.END}")
    click.echo(f"{Sp.OKBLUE}==================={Sp.END}")
    click.echo(" ")
    if name == "app":
        click.echo(f"{Sp.OKBLUE}Your app has the default name of 'app'{Sp.END}")
        click.echo(f"{Sp.OKBLUE}Flask will automatically look for this!{Sp.END}")
        click.echo(f"{Sp.OKBLUE}Run: flask run --debug{Sp.END}")
    else:
        click.echo(f"{Sp.OKBLUE}Your app has the name of '{name}'{Sp.END}")
        click.echo(f"{Sp.OKBLUE}Run: flask --app {name} run --debug{Sp.END}")
    click.echo(" ")
