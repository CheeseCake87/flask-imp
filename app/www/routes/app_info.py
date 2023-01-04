from flask import current_app, render_template

from app import bigapp
from .. import bp


@bp.route("/app-models", methods=["GET"])
def app_models():
    """
    Lists the model information loaded into bigapp.model_classes
    """
    models = bigapp.__model_registry__

    return render_template(
        bp.tmpl("app-models.html"),
        models=models
    )


@bp.route("/app-url-map", methods=["GET"])
def app_url_map():
    """
    Outputs all Flasks URLs
    """
    output = ""
    for rule in current_app.url_map.iter_rules():
        output += f"{rule.endpoint} : {rule.rule} <br/>"

    return render_template(
        bp.tmpl("app-url-map.html"),
        output=output,
    )
