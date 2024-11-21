import click

from .blueprint import add_api_blueprint as _add_api_blueprint
from .blueprint import add_blueprint as _add_blueprint
from .helpers import Sprinkles as Sp
from .init import init_app as _init_app
from .. import __version__


@click.group()
@click.version_option(__version__)
def cli() -> None:
    pass  # Entry Point


@cli.command("blueprint", help="Create a flask-imp blueprint")
@click.option(
    "-n",
    "--name",
    nargs=1,
    default="new_blueprint",
    prompt="Name",
    help="The name of the blueprint to create.",
)
@click.option(
    "-f",
    "--folder",
    nargs=1,
    default=".",
    prompt=(f"Folder {Sp.WARNING}(relative to CWD){Sp.END}"),
    help="The folder to create the blueprint in, creation is relative to the current working directory.",
)
def add_blueprint(name: str, folder: str) -> None:
    _add_blueprint(name=name, folder=folder)


@cli.command("api-blueprint", help="Create a flask-imp api blueprint")
@click.option(
    "-n",
    "--name",
    nargs=1,
    default="new_api_blueprint",
    prompt="Name",
    help="The name of the api blueprint to create.",
)
@click.option(
    "-f",
    "--folder",
    nargs=1,
    default=".",
    prompt=(f"Folder {Sp.WARNING}(relative to CWD){Sp.END}"),
    help="The folder to create the api blueprint in, creation is relative to the current working directory.",
)
def add_api_blueprint(name: str, folder: str) -> None:
    _add_api_blueprint(name=name, folder=folder)


@cli.command("init", help="Create a new flask-imp app.")
@click.option(
    "-n",
    "--name",
    nargs=1,
    default=None,
    help="The name of the app folder that will be created.",
)
@click.option("-s", "--slim", is_flag=True, default=False, help="Create a slim app.")
@click.option(
    "-m", "--minimal", is_flag=True, default=False, help="Create a minimal app."
)
@click.option("-f", "--full", is_flag=True, default=False, help="Create a full app.")
def init_new_app(name: str, full: bool, slim: bool, minimal: bool) -> None:
    if not full and not slim and not minimal:
        choice = click.prompt(
            "What type of app would you like to create?",
            default="minimal",
            type=click.Choice(["minimal", "slim", "full"]),
        )

        if choice == "full":
            full = True
        elif choice == "slim":
            slim = True
        elif choice == "minimal":
            minimal = True

    if name is None:
        set_name = click.prompt("What would you like to call your app?", default="app")

    else:
        set_name = name

    _init_app(set_name, full, slim, minimal)
