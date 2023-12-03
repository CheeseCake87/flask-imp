from pathlib import Path
from typing import Optional
import click

from .filelib import BlueprintFileLib as BpFlib
from .filelib import flask_imp_logo
from .filelib.head_tag_generator import head_tag_generator
from .filelib.main_js import main_js
from .filelib.water_css import water_css
from .helpers import Sprinkles as Sp
from .helpers import to_snake_case


def add_blueprint(folder, name, _init_app: bool = False, _cwd: Optional[Path] = None):
    click.echo(f"{Sp.OKGREEN}Creating Blueprint: {name}")

    if _cwd:
        cwd = _cwd

    else:
        if folder != "Current Working Directory":
            cwd = Path(Path.cwd() / folder)
        else:
            cwd = Path.cwd()

    if not cwd.exists():
        click.echo(f"{Sp.FAIL}{folder} does not exist.{Sp.END}")
        return

    name = to_snake_case(name)

    # Folders
    folders = {
        "root": cwd / name,
        "routes": cwd / name / "routes",
        "static": cwd / name / "static",
        "static/img": cwd / name / "static" / "img",
        "static/css": cwd / name / "static" / "css",
        "static/js": cwd / name / "static" / "js",
        "templates": cwd / name / "templates" / name,
        "templates/extends": cwd / name / "templates" / name / "extends",
        "templates/includes": cwd / name / "templates" / name / "includes",
    }

    # Files
    files = {
        "root/__init__.py": (folders["root"] / "__init__.py", BpFlib.init_py),
        "root/config.toml": (
            folders["root"] / "config.toml",
            BpFlib.config_toml.format(name=name, url_prefix="" if _init_app else name),
        ),
        "routes/index.py": (
            folders["routes"] / "index.py",
            BpFlib.routes_index_py.format(name=name),
        ),
        "static/img/flask-imp-logo.png": (
            folders["static/img"] / "flask-imp-logo.png",
            flask_imp_logo,
        ),
        "static/water.css": (folders["static/css"] / "water.css", water_css),
        "static/main.js": (
            folders["static/js"] / "main.js",
            main_js.format(main_js=folders["static"] / "main.js"),
        ),
        "templates/-/index.html": (
            folders["templates"] / "index.html",
            BpFlib.templates_index_html.format(
                root=folders["root"], name=name, flask_imp_logo=flask_imp_logo
            )
            if not _init_app
            else BpFlib.ia_templates_index_html.format(
                name=name,
                flask_imp_logo=flask_imp_logo,
                index_html=folders["templates"] / "index.html",
                extends_main_html=folders["templates/extends"] / "main.html",
                index_py=folders["routes"] / "index.py",
                init_py=folders["root"] / "__init__.py",
            ),
        ),
        "templates/-/extends/main.html": (
            folders["templates/extends"] / "main.html",
            BpFlib.templates_extends_main_html.format(
                name=name,
                head_tag=head_tag_generator(f"{name}.static"),
            ),
        ),
        "templates/-/includes/header.html": (
            folders["templates/includes"] / "header.html",
            BpFlib.templates_includes_header_html.format(
                header_html=folders["templates/includes"] / "header.html",
                main_html=folders["templates/extends"] / "main.html",
                static_path=f"{name}.static",
            ),
        ),
        "templates/-/includes/footer.html": (
            folders["templates/includes"] / "footer.html",
            BpFlib.templates_includes_footer_html.format(
                footer_html=folders["templates/includes"] / "footer.html",
                main_html=folders["templates/extends"] / "main.html",
            ),
        ),
    }

    # Loop create folders
    for folder, path in folders.items():
        if not path.exists():
            path.mkdir(parents=True)
            click.echo(f"{Sp.OKGREEN}Blueprint folder: {folder}, created{Sp.END}")
        else:
            click.echo(
                f"{Sp.WARNING}Blueprint folder already exists: {folder}, skipping{Sp.END}"
            )

    # Loop create files
    for file, (path, content) in files.items():
        if not path.exists():
            if file == "static/img/flask-imp-logo.png":
                path.write_bytes(bytes.fromhex(content))
                continue

            path.write_text(content, encoding="utf-8")

            click.echo(f"{Sp.OKGREEN}Blueprint file: {file}, created{Sp.END}")
        else:
            click.echo(
                f"{Sp.WARNING}Blueprint file already exists: {file}, skipping{Sp.END}"
            )

    click.echo(f"{Sp.OKGREEN}Blueprint created: {folders['root']}{Sp.END}")
