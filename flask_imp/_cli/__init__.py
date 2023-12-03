import click

from .blueprint import add_blueprint as _add_blueprint
from .helpers import Sprinkles as Sp
from .init import init_app as _init_app


@click.group()
def cli():
    pass  # Entry Point


@cli.command("blueprint", help="Create a flask-imp blueprint")
@click.option(
    "-f",
    "--folder",
    nargs=1,
    default="Current Working Directory",
    prompt=(
        f"\n{Sp.WARNING}(Creation is relative to the current working directory){Sp.END}\n"
        f"Folder to create blueprint in"
    ),
    help="The from_folder to create the blueprint in, defaults to the current working directory",
)
@click.option(
    "-n",
    "--name",
    nargs=1,
    default="my_new_blueprint",
    prompt="Name of the blueprint to create",
    help="The name of the blueprint to create",
)
def add_blueprint(folder, name):
    _add_blueprint(folder, name)


@cli.command("init", help="Create a new flask-imp app")
@click.option(
    "-n",
    "--name",
    nargs=1,
    default=None,
    help="The name of the app folder that will be created",
)
@click.option("-f", "--full", is_flag=True, default=False, help="Create a full app")
@click.option("-s", "--slim", is_flag=True, default=False, help="Create a slim app")
@click.option(
    "-m", "--minimal", is_flag=True, default=False, help="Create a minimal app"
)
def init_new_app(name, full, slim, minimal):
    if not full and not slim and not minimal:
        choice = click.prompt(
            "What type of app would you like to create?",
            default="full",
            type=click.Choice(["full", "slim", "minimal"]),
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

    if minimal:
        slim = True

    _init_app(set_name, full, slim, minimal)
