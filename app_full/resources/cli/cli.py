from flask import current_app as app


@app.cli.command("show-config")
def show_config():
    print(app.config)
