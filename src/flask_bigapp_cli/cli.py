import click

from .helpers import Sprinkles as Sp
from .blueprint import add_blueprint as _add_blueprint
from .init_new_app import init_new_app as _init_new_app


@click.group()
def cli():
    pass  # Entry Point


@cli.command("blueprint", help="Create a flask-bigapp blueprint")
@click.option(
    '-f', '--folder',
    nargs=1,
    default="Current Working Directory",
    prompt=(f'\n{Sp.WARNING}(Creation is relative to the current working directory){Sp.END}\n'
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
    _init_new_app(name)
