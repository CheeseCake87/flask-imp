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

    @app.cli.command("test")
    def tester():
        compiler(doc_path, markdown_path)

    @app.cli.command("compile")
    def compile_site():
        compiler(doc_path, markdown_path)

    @app.cli.command("recompile")
    def recompile_site():
        compiler(doc_path, markdown_path, recompile=True)

    @app.cli.command("new")
    def new_post():
        title = input("Title: ")
        filename = f"0000-00-00_{title.lower().replace(' ', '-') or 'untitled'}.md"
        with open(cwd / "markdown" / filename, mode="w") as file:
            file.write(
                f"""\
```
Publish = False
Date = set-on-compile
Title = {title.title() or "Untitled"}
Description = Description
````

start here...
""")

    return app
