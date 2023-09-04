from pathlib import Path

import click

from .helpers import Sprinkles as Sp
from .init_new_app_blueprint import init_new_app_blueprint as _init_new_app_blueprint

from .filelib.all_files import GlobalFileLib
from .filelib.app import AppFileLib
from .filelib.flask_bigapp_logo_svg import flask_bigapp_logo_svg
from .filelib.water_css import water_css


def init_new_app(name):
    cwd = Path.cwd()

    app_folder = cwd / name

    if app_folder.exists():
        click.echo(f"{Sp.FAIL}{name} folder already exists!{Sp.END}")
        click.confirm("Are you sure you want to continue?", abort=True)

    gc_folder = app_folder / "global"
    models_folder = app_folder / "models"
    blueprints_folder = app_folder / "blueprints"
    extensions_folder = app_folder / "extensions"

    app_folders = (
        app_folder,
        gc_folder,
        models_folder,
        blueprints_folder,
        extensions_folder
    )

    # Create app folders
    for folder in app_folders:
        if not folder.exists():
            folder.mkdir(parents=True)

    global_tlf = (
        "cli",
        "routes",
        "templates",
        "static",
        "context_processors",
        "error_handlers",
        "filters",
    )

    global_static_folders = (
        "css",
        "js",
        "img",
    )

    global_templates_folders = (
        "errors",
        "extends",
        "includes",
    )

    global_tlf_lookup = dict()

    # Prepare global folder structure
    for folder in global_tlf:
        global_tlf_lookup[folder] = gc_folder / folder
        this_folder = gc_folder / folder
        if not this_folder.exists():
            click.echo(f"{Sp.OKGREEN}Global collections folder: {this_folder.name}, created{Sp.END}")
            this_folder.mkdir(parents=True)

    # Prepare global static folders
    for folder in global_static_folders:
        this_folder = gc_folder / "static" / folder
        if not this_folder.exists():
            click.echo(
                f"{Sp.OKGREEN}Global collections static folder: {this_folder.name}, created{Sp.END}")
            this_folder.mkdir(parents=True)

    # Prepare global templates folders
    for folder in global_templates_folders:
        this_folder = gc_folder / "templates" / folder
        if not this_folder.exists():
            click.echo(
                f"{Sp.OKGREEN}Global collections templates folder: {this_folder.name}, created{Sp.END}")
            this_folder.mkdir(parents=True)

    app_files_lu = {
        "default.config.toml": (
            app_folder / "default.config.toml",
            AppFileLib.default_config_toml,
            {}
        ),
        "__init__.py": (
            app_folder / "__init__.py",
            AppFileLib.init_py,
            {"app_name": name}
        ),
    }

    # Model files lookup
    model_files_lu = {
        "__init__.py": (
            models_folder / "__init__.py",
            AppFileLib.models_init_py,
            {"app_name": name}
        ),
        "example_user_table.py": (
            models_folder / "example_user_table.py",
            AppFileLib.models_example_user_table_py,
            {}
        )
    }

    # Extensions files lookup
    extensions_files_lu = {
        "__init__.py": (
            extensions_folder / "__init__.py",
            AppFileLib.extensions_init_py,
            {}
        ),
    }

    global_file_lu = {
        "cli.py": (
            global_tlf_lookup["cli"] / "cli.py",
            GlobalFileLib.collections_cli_py,
            {"app_name": name}
        ),
        "context_processors.py": (
            global_tlf_lookup["context_processors"] / "context_processors.py",
            GlobalFileLib.collections_context_processors_py,
            {}
        ),
        "error_handlers.py": (
            global_tlf_lookup["error_handlers"] / "error_handlers.py",
            GlobalFileLib.collections_error_handlers_py,
            {}
        ),
        "filters.py": (
            global_tlf_lookup["filters"] / "filters.py",
            GlobalFileLib.collections_filters_py,
            {}
        ),
        "routes.py": (
            global_tlf_lookup["routes"] / "routes.py",
            GlobalFileLib.collections_routes_py,
            {}
        ),
        "water.css": (
            global_tlf_lookup["static"] / "css" / "water.css",
            water_css,
            {}
        ),
        "main.js": (
            global_tlf_lookup["static"] / "js" / "main.js",
            GlobalFileLib.static_main_js,
            {}
        ),
        "Flask-BigApp-Logo.svg": (
            global_tlf_lookup["static"] / "img" / "Flask-BigApp-Logo.svg",
            flask_bigapp_logo_svg,
            {}
        ),
        "index.html": (
            global_tlf_lookup["templates"] / "index.html",
            GlobalFileLib.templates_index_html,
            {}
        ),
        "400.html": (
            global_tlf_lookup["templates"] / "errors" / "400.html",
            GlobalFileLib.templates_errors_400_html,
            {}
        ),
        "401.html": (
            global_tlf_lookup["templates"] / "errors" / "401.html",
            GlobalFileLib.templates_errors_401_html,
            {}
        ),
        "403.html": (
            global_tlf_lookup["templates"] / "errors" / "403.html",
            GlobalFileLib.templates_errors_403_html,
            {}
        ),
        "404.html": (
            global_tlf_lookup["templates"] / "errors" / "404.html",
            GlobalFileLib.templates_errors_404_html,
            {}
        ),
        "405.html": (
            global_tlf_lookup["templates"] / "errors" / "405.html",
            GlobalFileLib.templates_errors_405_html,
            {}
        ),
        "500.html": (
            global_tlf_lookup["templates"] / "errors" / "500.html",
            GlobalFileLib.templates_errors_500_html,
            {}
        ),
        "main.html": (
            global_tlf_lookup["templates"] / "extends" / "main.html",
            GlobalFileLib.templates_extends_main_html,
            {}
        ),
        "footer.html": (
            global_tlf_lookup["templates"] / "includes" / "footer.html",
            GlobalFileLib.templates_includes_footer_html,
            {}
        ),
        "header.html": (
            global_tlf_lookup["templates"] / "includes" / "header.html",
            GlobalFileLib.templates_includes_header_html,
            {}
        ),
    }

    # Create app files
    for file_name, (file_path, file_content, formatter) in app_files_lu.items():
        if not file_path.exists():
            if formatter:
                file_path.write_text(file_content.format(**formatter), encoding="utf-8")
            else:
                file_path.write_text(file_content, encoding="utf-8")
            click.echo(f"{Sp.OKGREEN}App file: {file_name}, created{Sp.END}")
        else:
            click.echo(f"{Sp.WARNING}App file already exists: {file_path}, skipping{Sp.END}")

    # Create model files
    for file_name, (file_path, file_content, formatter) in model_files_lu.items():
        if not file_path.exists():
            if formatter:
                file_path.write_text(file_content.format(**formatter), encoding="utf-8")
            else:
                file_path.write_text(file_content, encoding="utf-8")
            click.echo(f"{Sp.OKGREEN}Model file: {file_name}, created{Sp.END}")
        else:
            click.echo(f"{Sp.WARNING}Model file already exists: {file_name}, skipping{Sp.END}")

    # Create extensions files
    for file_name, (file_path, file_content, formatter) in extensions_files_lu.items():
        if not file_path.exists():
            if formatter:
                file_path.write_text(file_content.format(**formatter), encoding="utf-8")
            else:
                file_path.write_text(file_content, encoding="utf-8")
            click.echo(f"{Sp.OKGREEN}Extensions file: {file_name}, created{Sp.END}")
        else:
            click.echo(f"{Sp.WARNING}Extensions file already exists: {file_path}, skipping{Sp.END}")

    # Prepare global folder files
    for file_name, (file_path, file_content, formatter) in global_file_lu.items():
        if not file_path.exists():
            if formatter:
                file_path.write_text(file_content.format(**formatter), encoding="utf-8")
            else:
                file_path.write_text(file_content, encoding="utf-8")
            click.echo(f"{Sp.OKGREEN}Global collections file: {file_name}, created{Sp.END}")
        else:
            click.echo(
                f"{Sp.WARNING}Global collections file already exists: {file_path}, skipping{Sp.END}")

    _init_new_app_blueprint(f"{name}/blueprints", "www")

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
