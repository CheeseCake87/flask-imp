from pathlib import Path

from flask import Flask

from .ssg import compiler

cwd = Path(__file__).parent


def create_app():
    app = Flask(__name__)
    app.static_folder = "static"
    app.template_folder = "templates"

    doc_path = cwd.parent / "docs"
    markdown_path = cwd / "markdown"

    @app.cli.command("compile")
    def compile_site():
        compiler(doc_path, markdown_path)

    return app
