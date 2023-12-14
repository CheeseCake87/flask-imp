from pathlib import Path
from time import sleep

import click
from flask import Flask

from .ssg import compiler
from .ssg.helpers import pytz_dt_epoch

cwd = Path(__file__).parent


def create_app():
    app = Flask(__name__)
    app.static_folder = "static"
    app.template_folder = "templates"

    doc_path = cwd.parent / "docs"
    markdown_path = cwd.parent / "docs_md"

    @app.cli.command("compile")
    @click.option("--watch", is_flag=True, help="Watch for file changes")
    def compile_site(watch):
        if watch:
            watching_files = {}

            def change_loop():
                change = False
                updated = []
                for file in markdown_path.glob("**/*.md"):
                    if file not in watching_files:
                        watching_files[file] = file.stat().st_mtime
                        updated.append(file)
                        change = True
                    else:
                        if file.stat().st_mtime > watching_files[file]:
                            watching_files[file] = file.stat().st_mtime
                            updated.append(file)
                            change = True

                if change:
                    print("Update detected, recompiling...")
                    for file in updated:
                        print(f" - {file}")

                    compiler(doc_path, markdown_path)

                    print("Watching for changes...")

            while True:
                change_loop()
                sleep(1)

        else:
            compiler(doc_path, markdown_path)

    @app.route("/")
    def index():
        return "To use run the following command: flask --app gdocs compile"

    return app
