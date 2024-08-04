from flask_imp import ImpBlueprint, ImpBlueprintConfig, DatabaseConfig

bp = ImpBlueprint(__name__, ImpBlueprintConfig(
    enabled=True,
    url_prefix="/",
    static_folder="static",
    template_folder="templates",
    static_url_path="/static",
    init_session={"www_session": "yes"},
    database_binds=(
        DatabaseConfig(
            enabled=True,
            dialect="sqlite",
            name="www",
            bind_key="www",
            location="",
            port=0,
            username="",
            password="",
        ),
    ),
))

bp.import_resources("routes")
bp.import_models("models")


@bp.before_app_request
def before_app_request():
    bp.init_session()
