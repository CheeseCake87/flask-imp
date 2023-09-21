from pathlib import Path
from time import sleep

from flask import Flask

from .ssg import compiler
from .ssg.helpers import pytz_dt_epoch

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

    @app.cli.command("watch")
    def watch_for_changes():
        print("Watching for changes...")

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

        while True:
            change_loop()
            sleep(1)

    return app
