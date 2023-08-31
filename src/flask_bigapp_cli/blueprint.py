from pathlib import Path
import click

from .helpers import to_snake_case
from .helpers import Sprinkles as Sp
from .filelib import BlueprintFileLib
from .filelib import flask_bigapp_logo_svg
from .filelib import water_css


def add_blueprint(folder, name, _root=False, _from_init=False):
    cwd = Path.cwd()
    if folder != "Current Working Directory":
        cwd = Path(cwd / folder)
    if not cwd.exists():
        click.echo(
            f"{Sp.FAIL}{folder} does not exist.{Sp.END}")
        return

    name = to_snake_case(name)

    # Prepare blueprint folder structure
    bp_folder = cwd / name
    bp_routes_folder = bp_folder / "routes"
    bp_templates_folder = bp_folder / "templates" / name
    bp_templates_extends_folder = bp_templates_folder / "extends"
    bp_static_folder = bp_folder / "static"

    # Prepare blueprint files
    bp_init_py = bp_folder / "__init__.py"
    bp_config_toml = bp_folder / "config.toml"
    bp_routes_index_py = bp_routes_folder / "index.py"
    bp_templates_index_html = bp_templates_folder / "index.html"
    bp_templates_extends_main_html = bp_templates_extends_folder / "main.html"
    bp_static_water_css = bp_static_folder / "water.css"
    bp_static_flask_bigapp_logo_svg = bp_static_folder / "Flask-BigApp-Logo.svg"

    # Prepare blueprint folders for loop creation
    folders = (
        bp_folder,
        bp_routes_folder,
        bp_templates_folder,
        bp_templates_extends_folder,
        bp_static_folder,
    )

    # Loop create folders
    for folder in folders:
        if not folder.exists():
            folder.mkdir(parents=True)
            click.echo(f"{Sp.OKGREEN}Blueprint folder: {folder.name}, created{Sp.END}")
        else:
            click.echo(f"{Sp.WARNING}Blueprint folder already exists: {folder.name}, skipping{Sp.END}")

    # Create __init__.py
    if not bp_init_py.exists():
        bp_init_py.write_text(BlueprintFileLib.init_py, encoding="utf-8")
        click.echo(f"{Sp.OKGREEN}Blueprint __init__ created{Sp.END}")
    else:
        click.echo(f"{Sp.WARNING}Blueprint __init__ already exists, skipping{Sp.END}")

    # Create config.toml
    if not bp_config_toml.exists():
        bp_config_toml.write_text(
            BlueprintFileLib.config_toml.format(
                name=name,
                url_prefix=name if not _root else "",
            ), encoding="utf-8"
        )
        click.echo(f"{Sp.OKGREEN}Blueprint config, created{Sp.END}")
    else:
        click.echo(f"{Sp.WARNING}Blueprint config already exists, skipping{Sp.END}")

    # Create blueprint index.py route
    if not bp_routes_index_py.exists():
        bp_routes_index_py.write_text(
            BlueprintFileLib.routes_index_py, encoding="utf-8")
        click.echo(f"{Sp.OKGREEN}Blueprint route: {bp_routes_index_py.name}, created{Sp.END}")
    else:
        click.echo(f"{Sp.WARNING}Blueprint route already exists: {bp_routes_index_py.name}, skipping{Sp.END}")

    # Create blueprint index.html template
    if not bp_templates_index_html.exists():
        bp_templates_index_html.write_text(
            BlueprintFileLib.templates_index_html.format(name=name), encoding="utf-8")
        click.echo(f"{Sp.OKGREEN}Blueprint template file: {bp_templates_index_html.name}, created{Sp.END}")
    else:
        click.echo(
            f"{Sp.WARNING}Blueprint template file already exists: {bp_templates_index_html.name}, skipping{Sp.END}")

    # Create blueprint main.html extend template
    if not bp_templates_extends_main_html.exists():
        bp_templates_extends_main_html.write_text(
            BlueprintFileLib.templates_extends_main_html.format(name=name), encoding="utf-8")
        click.echo(f"{Sp.OKGREEN}Blueprint template file: {bp_templates_extends_main_html.name}, created{Sp.END}")
    else:
        click.echo(
            f"{Sp.WARNING}Blueprint template file already exists: {bp_templates_extends_main_html.name}, skipping{Sp.END}")

    # Create logo
    if not bp_static_flask_bigapp_logo_svg.exists():
        bp_static_flask_bigapp_logo_svg.write_text(
            flask_bigapp_logo_svg, encoding="utf-8")
        click.echo(f"{Sp.OKGREEN}Blueprint static image: {bp_static_flask_bigapp_logo_svg.name}, created{Sp.END}")
    else:
        click.echo(
            f"{Sp.WARNING}Blueprint static image already \
            exists: {bp_static_flask_bigapp_logo_svg.name}, skipping{Sp.END}")

    # Create water.css
    if not bp_static_water_css.exists():
        bp_static_water_css.write_text(
            water_css, encoding="utf-8")
        click.echo(f"{Sp.OKGREEN}Blueprint static image: {bp_static_water_css.name}, created{Sp.END}")
    else:
        click.echo(
            f"{Sp.WARNING}Blueprint static image already \
            exists: {bp_static_water_css.name}, skipping{Sp.END}")

    click.echo(f"{Sp.OKGREEN}Blueprint created: {bp_folder}{Sp.END}")
