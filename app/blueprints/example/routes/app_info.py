from flask import current_app, render_template
from app import bigapp

from .. import bp, page_needs


@bp.route("/app-models", methods=["GET"])
def app_models():
    """
    Lists the model information loaded into bigapp.model_classes
    """
    models = bigapp.model_classes

    render = bp.tmpl("app-models.html")
    return render_template(render, models=models, **page_needs)


@bp.route("/app-url-map", methods=["GET"])
def app_url_map():
    """
    Outputs all Flasks URLs
    """
    output = ""
    for rule in current_app.url_map.iter_rules():
        output += f"{rule.endpoint} : {rule.rule} <br/>"

    render = bp.tmpl("app-url-map.html")
    return render_template(render, output=output, **page_needs)
