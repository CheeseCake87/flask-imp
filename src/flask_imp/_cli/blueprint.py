import typing as t
from pathlib import Path

import click

from .filelib.head_tag_generator import head_tag_generator
from .filelib.main_js import main_js
from .filelib.water_css import water_css
from .helpers import Sprinkles as Sp
from .helpers import build
from .helpers import to_snake_case


def add_api_blueprint(
    name: str = "new_api_blueprint",
    folder: str = ".",
    _init_app: bool = False,
    _cwd: t.Optional[Path] = None,
    _url_prefix: t.Optional[str] = None,
) -> None:
    from .filelib.api_blueprint import api_blueprint_init_py
    from .filelib.api_blueprint import api_blueprint_resources_index_py

    click.echo(f"{Sp.OKGREEN}Creating API Blueprint: {name}")

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

    folders: t.Dict[str, Path] = {
        "root": root_folder,
        "resources": root_folder / "resources",
    }

    files: t.Dict[str, t.Tuple[Path, t.Any]] = {
        "root/__init__.py": (
            folders["root"] / "__init__.py",
            api_blueprint_init_py(
                url_prefix=name if not _url_prefix else _url_prefix, name=name
            ),
        ),
        "resources/index.py": (
            folders["resources"] / "index.py",
            api_blueprint_resources_index_py(),
        ),
    }

    build(folders, files, building="API Blueprint")


def add_blueprint(
    name: str = "new_blueprint",
    folder: str = ".",
    _init_app: bool = False,
    _cwd: t.Optional[Path] = None,
    _url_prefix: t.Optional[str] = None,
) -> None:
    from .filelib.blueprint import blueprint_init_py
    from .filelib.blueprint import blueprint_resources_index_py
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

    folders: t.Dict[str, Path] = {
        "root": root_folder,
        "resources": root_folder / "resources",
        "static": root_folder / "static",
        "static/css": root_folder / "static" / "css",
        "static/js": root_folder / "static" / "js",
        "templates": root_folder / "templates" / name,
        "templates/extends": root_folder / "templates" / name / "extends",
        "templates/includes": root_folder / "templates" / name / "includes",
    }

    files: t.Dict[str, t.Tuple[Path, t.Any]] = {
        "root/__init__.py": (
            folders["root"] / "__init__.py",
            blueprint_init_py(
                url_prefix=name if not _url_prefix else _url_prefix, name=name
            ),
        ),
        "resources/index.py": (
            folders["resources"] / "index.py",
            blueprint_resources_index_py(),
        ),
        "static/water.css": (folders["static/css"] / "water.css", water_css),
        "static/main.js": (
            folders["static/js"] / "main.js",
            main_js(main_js_=folders["static"] / "main.js"),
        ),
        "templates/-/index.html": (
            folders["templates"] / "index.html",
            blueprint_templates_index_html(root=folders["root"], blueprint_name=name)
            if not _init_app
            else blueprint_init_app_templates_index_html(
                blueprint_name=name,
                index_html=folders["templates"] / "index.html",
                extends_main_html=folders["templates/extends"] / "main.html",
                index_py=folders["resources"] / "index.py",
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

    build(folders, files, building="Blueprint")
