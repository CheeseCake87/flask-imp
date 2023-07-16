from pathlib import Path

import click

from flask_bigapp.resources import Resources
from .helpers import Sprinkles, _add_blueprint
from .resources import Resources as CLIResources


@click.group()
def cli():
    pass  # Entry Point


@cli.command("blueprint", help="Create a flask-bigapp blueprint")
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
    _add_blueprint(folder, name)


@cli.command("init", help="Create a new flask-bigapp app")
@click.option(
    '-n', '--name',
    nargs=1,
    default="app",
    prompt='What would you like to call your app?',
    help='The name of the app folder that will be created'
)
def init_new_app(name):
    cwd = Path.cwd()

    app_folder = cwd / name

    if app_folder.exists():
        click.echo(f"{Sprinkles.FAIL}{name} folder already exists!{Sprinkles.END}")
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
            click.echo(f"{Sprinkles.OKGREEN}Global collections folder: {this_folder.name}, created{Sprinkles.END}")
            this_folder.mkdir(parents=True)

    # Prepare global static folders
    for folder in global_static_folders:
        this_folder = gc_folder / "static" / folder
        if not this_folder.exists():
            click.echo(
                f"{Sprinkles.OKGREEN}Global collections static folder: {this_folder.name}, created{Sprinkles.END}")
            this_folder.mkdir(parents=True)

    # Prepare global templates folders
    for folder in global_templates_folders:
        this_folder = gc_folder / "templates" / folder
        if not this_folder.exists():
            click.echo(
                f"{Sprinkles.OKGREEN}Global collections templates folder: {this_folder.name}, created{Sprinkles.END}")
            this_folder.mkdir(parents=True)

    app_files_lu = {
        "default.config.toml": (
            app_folder / "default.config.toml",
            Resources.default_config,
            {}
        ),
        "__init__.py": (
            app_folder / "__init__.py",
            CLIResources.app_init,
            {"app_name": name}
        ),
    }

    # Model files lookup
    model_files_lu = {
        "__init__.py": (
            models_folder / "__init__.py",
            CLIResources.models_init,
            {"app_name": name}
        ),
        "example__table.py": (
            models_folder / "example__table.py",
            CLIResources.models_example_table,
            {}
        )
    }

    # Extensions files lookup
    extensions_files_lu = {
        "__init__.py": (
            extensions_folder / "__init__.py",
            CLIResources.extensions_init,
            {}
        ),
    }

    global_file_lu = {
        "cli.py": (
            global_tlf_lookup["cli"] / "cli.py",
            CLIResources.global_cli_py,
            {"app_name": name}
        ),
        "context_processors.py": (
            global_tlf_lookup["context_processors"] / "context_processors.py",
            CLIResources.global_context_processors_py,
            {}
        ),
        "error_handlers.py": (
            global_tlf_lookup["error_handlers"] / "error_handlers.py",
            CLIResources.global_error_handlers_py,
            {}
        ),
        "filters.py": (
            global_tlf_lookup["filters"] / "filters.py",
            CLIResources.global_filters_py,
            {}
        ),
        "routes.py": (
            global_tlf_lookup["routes"] / "routes.py",
            CLIResources.global_routes_py,
            {}
        ),
        "main.css": (
            global_tlf_lookup["static"] / "css" / "main.css",
            CLIResources.global_static_main_css,
            {}
        ),
        "main.js": (
            global_tlf_lookup["static"] / "js" / "main.js",
            CLIResources.global_static_main_js,
            {}
        ),
        "Flask-BigApp-Logo.svg": (
            global_tlf_lookup["static"] / "img" / "Flask-BigApp-Logo.svg",
            CLIResources.global_static_logo_svg,
            {}
        ),
        "index.html": (
            global_tlf_lookup["templates"] / "index.html",
            CLIResources.index_html,
            {}
        ),
        "400.html": (
            global_tlf_lookup["templates"] / "errors" / "400.html",
            CLIResources.page_400,
            {}
        ),
        "401.html": (
            global_tlf_lookup["templates"] / "errors" / "401.html",
            CLIResources.page_401,
            {}
        ),
        "403.html": (
            global_tlf_lookup["templates"] / "errors" / "403.html",
            CLIResources.page_403,
            {}
        ),
        "404.html": (
            global_tlf_lookup["templates"] / "errors" / "404.html",
            CLIResources.page_404,
            {}
        ),
        "405.html": (
            global_tlf_lookup["templates"] / "errors" / "405.html",
            CLIResources.page_405,
            {}
        ),
        "500.html": (
            global_tlf_lookup["templates"] / "errors" / "500.html",
            CLIResources.page_500,
            {}
        ),
        "main.html": (
            global_tlf_lookup["templates"] / "extends" / "main.html",
            CLIResources.extends_main,
            {}
        ),
        "footer.html": (
            global_tlf_lookup["templates"] / "includes" / "footer.html",
            CLIResources.includes_footer,
            {}
        ),
        "header.html": (
            global_tlf_lookup["templates"] / "includes" / "header.html",
            CLIResources.includes_header,
            {}
        ),
    }

    # Create app files
    for file_name, (file_path, file_content, formatter) in app_files_lu.items():
        if not file_path.exists():
            if formatter:
                file_path.write_text(file_content.format(**formatter))
            else:
                file_path.write_text(file_content)
            click.echo(f"{Sprinkles.OKGREEN}App file: {file_name}, created{Sprinkles.END}")
        else:
            click.echo(f"{Sprinkles.WARNING}App file already exists: {file_path}, skipping{Sprinkles.END}")

    # Create model files
    for file_name, (file_path, file_content, formatter) in model_files_lu.items():
        if not file_path.exists():
            if formatter:
                file_path.write_text(file_content.format(**formatter))
            else:
                file_path.write_text(file_content)
            click.echo(f"{Sprinkles.OKGREEN}Model file: {file_name}, created{Sprinkles.END}")
        else:
            click.echo(f"{Sprinkles.WARNING}Model file already exists: {file_name}, skipping{Sprinkles.END}")

    # Create extensions files
    for file_name, (file_path, file_content, formatter) in extensions_files_lu.items():
        if not file_path.exists():
            if formatter:
                file_path.write_text(file_content.format(**formatter))
            else:
                file_path.write_text(file_content)
            click.echo(f"{Sprinkles.OKGREEN}Extensions file: {file_name}, created{Sprinkles.END}")
        else:
            click.echo(f"{Sprinkles.WARNING}Extensions file already exists: {file_path}, skipping{Sprinkles.END}")

    # Prepare global folder files
    for file_name, (file_path, file_content, formatter) in global_file_lu.items():
        if not file_path.exists():
            if formatter:
                file_path.write_text(file_content.format(**formatter))
            else:
                file_path.write_text(file_content)
            click.echo(f"{Sprinkles.OKGREEN}Global collections file: {file_name}, created{Sprinkles.END}")
        else:
            click.echo(
                f"{Sprinkles.WARNING}Global collections file already exists: {file_path}, skipping{Sprinkles.END}")

    _add_blueprint(f"{name}/blueprints", "www", _root=True)

    click.echo(" ")
    click.echo(f"{Sprinkles.OKBLUE}==================={Sprinkles.END}")
    click.echo(f"{Sprinkles.OKBLUE}Flask app deployed!{Sprinkles.END}")
    click.echo(f"{Sprinkles.OKBLUE}==================={Sprinkles.END}")
    click.echo(" ")
    click.echo(f"{Sprinkles.OKGREEN}'/' route is set by the blueprint named www{Sprinkles.END}")
    click.echo(f"{Sprinkles.OKGREEN}found in the blueprints folder. It is encouraged{Sprinkles.END}")
    click.echo(f"{Sprinkles.OKGREEN}to use blueprints to set all app routes.{Sprinkles.END}")
    click.echo(" ")
    click.echo(f"{Sprinkles.OKGREEN}All app (non-blueprint) resources can be found{Sprinkles.END}")
    click.echo(f"{Sprinkles.OKGREEN}in the global folder. Have a look through this{Sprinkles.END}")
    click.echo(f"{Sprinkles.OKGREEN}folder to find out more.{Sprinkles.END}")
    click.echo(" ")
    if name == 'app':
        click.echo(f"{Sprinkles.OKBLUE}Your app has the default name of 'app'{Sprinkles.END}")
        click.echo(f"{Sprinkles.OKBLUE}Flask will automatically look for this!{Sprinkles.END}")
        click.echo(f"{Sprinkles.OKBLUE}Run: Flask run --debug{Sprinkles.END}")
    else:
        click.echo(f"{Sprinkles.OKBLUE}Your app has the name of '{name}'{Sprinkles.END}")
        click.echo(f"{Sprinkles.OKBLUE}Run: Flask --app {name} run --debug{Sprinkles.END}")
