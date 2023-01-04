import re
from pathlib import Path

import click

from .resources import Resources


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


@cli.command("add-bp", help="Create a flask-bigapp blueprint")
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
@click.option(
    '-urlp', '--url-prefix',
    nargs=1,
    default="/",
    prompt='URL prefix',
    help='The URL Prefix to set for the blueprint'
)
@click.option(
    '-surlp', '--static-url-path',
    nargs=1,
    default="/<blueprint_name>/static",
    prompt='Static URL path',
    help='The URL Prefix to set for the blueprint'
)
def add_blueprint(folder, name, url_prefix, static_url_path):
    cwd = Path.cwd()
    if folder != "Current Working Directory":
        cwd = Path(cwd / folder)
    if not cwd.exists():
        click.echo(
            f"{Sprinkles.FAIL}{folder} does not exist.{Sprinkles.END}")
        return

    name = to_snake_case(name)

    url_prefix = url_prefix if url_prefix != "/" else "/"
    url_prefix = url_prefix if url_prefix.startswith("/") else f"/{url_prefix}"

    if static_url_path == "/<blueprint_name>/static":
        static_url_path = f"/{name}/static"
    else:
        static_url_path = static_url_path if static_url_path.startswith("/") else f"/{static_url_path}"

    bp_folder = cwd / name
    bp_routes_folder = bp_folder / "routes"
    bp_templates_folder = bp_folder / "templates" / name
    bp_static_folder = bp_folder / "static"

    bp_init = bp_folder / "__init__.py"
    bp_config = bp_folder / "config.toml"
    bp_route = bp_routes_folder / "index.py"
    bp_template = bp_templates_folder / "index.html"

    folders = [bp_folder, bp_routes_folder, bp_templates_folder, bp_static_folder]

    for folder in folders:
        if not folder.exists():
            folder.mkdir(parents=True)
        else:
            click.echo(f"{Sprinkles.WARNING}Folder already exists: {folder}, skipping{Sprinkles.END}")

    if not bp_init.exists():
        bp_init.write_text(Resources.blueprint_init)
    else:
        click.echo(f"{Sprinkles.WARNING}__init__ already exists: {bp_init}, skipping{Sprinkles.END}")

    if not bp_config.exists():
        bp_config.write_text(
            Resources.blueprint_config.format(
                name=name,
                url_prefix=url_prefix,
                static_url_path=static_url_path
            )
        )
    else:
        click.echo(f"{Sprinkles.WARNING}Config already exists: {bp_config}, skipping{Sprinkles.END}")

    if not bp_route.exists():
        bp_route.write_text(Resources.blueprint_index_route)
    else:
        click.echo(f"{Sprinkles.WARNING}Route already exists: {bp_route}, skipping{Sprinkles.END}")

    if not bp_template.exists():
        bp_template.write_text(Resources.blueprint_index_template.format(name=name))
    else:
        click.echo(f"{Sprinkles.WARNING}Template already exists: {bp_template}, skipping{Sprinkles.END}")

    click.echo(f"{Sprinkles.OKGREEN}Blueprint created: {bp_folder}{Sprinkles.END}")


@cli.command("rename-bp", help="Rename a flask-bigapp blueprint")
@click.option(
    '-bp', '--blueprint',
    nargs=1,
    prompt=(
            f'\n{Sprinkles.WARNING}(Search of the blueprint is relative to the current working directory){Sprinkles.END}\n'
            f'\nMust be the blueprint from_folder (that contains the __init__.py file)\n'
            f'Blueprint to rename'
    ),
    help='Location of the blueprint to rename'
)
@click.option(
    '-n', '--new-name',
    nargs=1,
    prompt='New name',
    help='The new name to give to the blueprint'
)
def rename_blueprint(blueprint, new_name):
    cwd = Path.cwd()
    blueprint_path = Path(cwd / blueprint)
    if not blueprint_path.exists():
        click.echo(
            f"{Sprinkles.FAIL}The Blueprint [{blueprint}] does not exist in the {blueprint_path.parent} directory.{Sprinkles.END}")
        return

    blueprint_nested_template_path = blueprint_path / "templates" / blueprint_path.name

    new_name = to_snake_case(new_name)

    new_path = blueprint_path.parent / new_name

    if new_path.exists():
        click.echo(f"{Sprinkles.FAIL}The new name you have given already exists.{Sprinkles.END}")
        return

    blueprint_config = blueprint_path / "config.toml"

    with open(blueprint_config, "r") as f:
        config = f.read()

    config = config.replace(blueprint_path.name, new_name)

    with open(blueprint_config, "w") as f:
        f.write(config)

    blueprint_nested_template_path.rename(blueprint_path / "templates" / new_name)
    blueprint_path.rename(blueprint_path.parent / new_name)


@cli.command("add-theme", help="Create a flask-bigapp theme")
@click.option(
    '-f', '--from_folder',
    nargs=1,
    default="Current Working Directory",
    prompt=(f'\n{Sprinkles.WARNING}(Creation is relative to the current working directory){Sprinkles.END}\n'
            f'Folder to create theme in'),
    help='The from_folder to create the theme in, defaults to the current working directory'
)
@click.option(
    '-n', '--name',
    nargs=1,
    default="my_new_theme",
    prompt='Name of the theme to create',
    help='The name of the theme to create'
)
@click.option(
    '-surlp', '--static-url-path',
    nargs=1,
    default="/<theme_name>/static",
    prompt='Static URL path',
    help='The URL Prefix to set for the theme'
)
def add_theme(folder, name, static_url_path):
    import shutil

    cwd = Path.cwd()

    if folder != "Current Working Directory":
        cwd = Path(cwd / folder)
    if not cwd.exists():
        click.echo(
            f"{Sprinkles.FAIL}{folder} does not exist.{Sprinkles.END}")
        return

    name = to_snake_case(name)

    theme_folder = cwd / name

    if theme_folder.exists():
        click.echo(f"{Sprinkles.WARNING}Theme already exists: {theme_folder}, skipping{Sprinkles.END}")
        return

    if static_url_path != "/<theme_name>/static":
        static_url_path = static_url_path if static_url_path.startswith("/") else f"/{static_url_path}"
    else:
        static_url_path = f"/{name}/static"

    temp_them_folder = cwd / "__temp_theme_dir__"
    temp_theme_nested_template_folder = temp_them_folder / "templates" / "__temp_theme_dir__"

    rename_theme_folder = cwd / name
    rename_theme_nested_template_folder = temp_them_folder / "templates" / name

    new_theme_folder = rename_theme_folder
    new_theme_nested_template_folder = new_theme_folder / "templates" / name

    cli_dir = Path(__file__).parent
    cli_theme_dir = cli_dir / "__temp_theme_dir__"

    shutil.copytree(cli_theme_dir, temp_them_folder, dirs_exist_ok=True)

    theme_config = temp_them_folder / "config.toml"
    theme_main = new_theme_nested_template_folder / "extends" / "main.html"

    if not theme_config.exists():
        theme_config.write_text(
            Resources.theme_config.format(
                name=name,
                static_url_path=static_url_path
            )
        )
    else:
        click.echo(f"{Sprinkles.WARNING}Config already exists: {theme_config}, skipping{Sprinkles.END}")

    temp_theme_nested_template_folder.rename(rename_theme_nested_template_folder)
    temp_them_folder.rename(rename_theme_folder)

    with open(theme_main, "r") as f:
        main = f.read()

    main = main.replace("__temp_theme_dir__", name)

    with open(theme_main, "w") as f:
        f.write(main)

    click.echo(f"{Sprinkles.OKGREEN}Theme created: {theme_folder}{Sprinkles.END}")


@cli.command("rename-theme", help="Rename a flask-bigapp theme")
@click.option(
    '-t', '--theme',
    nargs=1,
    prompt=(
            f'\n{Sprinkles.WARNING}(Search of the theme is relative to the current working directory){Sprinkles.END}\n'
            f'Theme to rename'
    ),
    help='Location of the theme to rename'
)
@click.option(
    '-n', '--new-name',
    nargs=1,
    prompt='New name',
    help='The new name to give to the theme'
)
def rename_theme(theme, new_name):
    cwd = Path.cwd()
    theme_path = Path(cwd / theme)
    if not theme_path.exists():
        click.echo(
            f"{Sprinkles.FAIL}The Theme [{theme}] does not exist in the {theme_path.parent} directory.{Sprinkles.END}")
        return

    theme_nested_template_path = theme_path / "templates" / theme_path.name

    new_name = to_snake_case(new_name)
    new_path = theme_path.parent / new_name

    if new_path.exists():
        click.echo(f"{Sprinkles.FAIL}The new name you have given already exists.{Sprinkles.END}")
        return

    theme_config = theme_path / "config.toml"

    with open(theme_config, "r") as f:
        config = f.read()

    config = config.replace(theme_path.name, new_name)

    with open(theme_config, "w") as f:
        f.write(config)

    theme_nested_template_path.rename(theme_path / "templates" / new_name)
    theme_path.rename(theme_path.parent / new_name)
