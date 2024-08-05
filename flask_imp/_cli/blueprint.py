from pathlib import Path
from typing import Optional

import click

from .filelib.flask_imp_logo import flask_imp_logo
from .filelib.head_tag_generator import head_tag_generator
from .filelib.main_js import main_js
from .filelib.water_css import water_css
from .helpers import Sprinkles as Sp
from .helpers import to_snake_case


def add_blueprint(
        name: str = "new_blueprint",
        folder: str = ".",
        _init_app: bool = False,
        _cwd: Optional[Path] = None,
        _url_prefix: Optional[str] = None,
):
    from .filelib.blueprint import blueprint_init_py
    from .filelib.blueprint import blueprint_routes_index_py
    from .filelib.blueprint import blueprint_templates_index_html
    from .filelib.blueprint import blueprint_init_app_templates_index_html
    from .filelib.blueprint import blueprint_templates_extends_main_html
    from .filelib.blueprint import blueprint_templates_includes_header_html
    from .filelib.blueprint import blueprint_templates_includes_footer_html

    click.echo(f"{Sp.OKGREEN}Creating Blueprint: {name}")

    if _cwd:
        cwd = _cwd
    else:
        cwd = Path.cwd()

    if not cwd.exists():
        click.echo(f"{Sp.FAIL}{folder} does not exist.{Sp.END}")
        return

    name = to_snake_case(name)

    if folder == ".":
        root_folder = cwd / name
    else:
        root_folder = cwd / folder / name

    folders = {
        "root": root_folder,
        "routes": root_folder / "routes",
        "static": root_folder / "static",
        "static/img": root_folder / "static" / "img",
        "static/css": root_folder / "static" / "css",
        "static/js": root_folder / "static" / "js",
        "templates": root_folder / "templates" / name,
        "templates/extends": root_folder / "templates" / name / "extends",
        "templates/includes": root_folder / "templates" / name / "includes",
    }

    files = {
        "root/__init__.py": (
            folders["root"] / "__init__.py",
            blueprint_init_py(url_prefix=name if not _url_prefix else _url_prefix, name=name),
        ),
        "routes/index.py": (
            folders["routes"] / "index.py",
            blueprint_routes_index_py(),
        ),
        "static/img/flask-imp-logo.png": (
            folders["static/img"] / "flask-imp-logo.png",
            flask_imp_logo,
        ),
        "static/water.css": (folders["static/css"] / "water.css", water_css),
        "static/main.js": (
            folders["static/js"] / "main.js",
            main_js(main_js_=folders["static"] / "main.js"),
        ),
        "templates/-/index.html": (
            folders["templates"] / "index.html",
            blueprint_templates_index_html(
                root=folders["root"], name=name
            )
            if not _init_app
            else blueprint_init_app_templates_index_html(
                name=name,
                index_html=folders["templates"] / "index.html",
                extends_main_html=folders["templates/extends"] / "main.html",
                index_py=folders["routes"] / "index.py",
                init_py=folders["root"] / "__init__.py",
            ),
        ),
        "templates/-/extends/main.html": (
            folders["templates/extends"] / "main.html",
            blueprint_templates_extends_main_html(
                name=name,
                head_tag=head_tag_generator(f"{name}.static"),
            ),
        ),
        "templates/-/includes/header.html": (
            folders["templates/includes"] / "header.html",
            blueprint_templates_includes_header_html(
                header_html=folders["templates/includes"] / "header.html",
                main_html=folders["templates/extends"] / "main.html",
                static_path=f"{name}.static",
            ),
        ),
        "templates/-/includes/footer.html": (
            folders["templates/includes"] / "footer.html",
            blueprint_templates_includes_footer_html(
                footer_html=folders["templates/includes"] / "footer.html",
                main_html=folders["templates/extends"] / "main.html",
            ),
        ),
    }

    for folder, path in folders.items():
        if not path.exists():
            path.mkdir(parents=True)
            click.echo(f"{Sp.OKGREEN}Blueprint folder: {folder}, created{Sp.END}")
        else:
            click.echo(
                f"{Sp.WARNING}Blueprint folder already exists: {folder}, skipping{Sp.END}"
            )

    for file, (path, content) in files.items():
        if not path.exists():
            if file == "static/img/flask-imp-logo.png":
                path.write_bytes(bytes.fromhex(content))
                continue

            if not content:
                print(path)
            path.write_text(content, encoding="utf-8")

            click.echo(f"{Sp.OKGREEN}Blueprint file: {file}, created{Sp.END}")
        else:
            click.echo(
                f"{Sp.WARNING}Blueprint file already exists: {file}, skipping{Sp.END}"
            )

    click.echo(f"{Sp.OKGREEN}Blueprint created: {folders['root']}{Sp.END}")
