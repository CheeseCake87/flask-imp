from flask import current_app as app
from flask import render_template


@app.route("/global")
def index():
    return render_template(
        "index.html",
    )
