class Resources:
    # Format to: NONE
    blueprint_init = """\
from flask_bigapp import Blueprint

bp = Blueprint(__name__)

bp.import_routes("routes")


@bp.before_app_request
def before_app_request():
    bp.init_session()

"""

    # Format to: name, static_url_path, url_prefix
    blueprint_config = """\
enabled = "yes"

[settings]
url_prefix = "{url_prefix}"
subdomain = ""
url_defaults = {{}}
static_folder = "static"
template_folder = "templates"
static_url_path = "{static_url_path}"

[session]
{name}_session = "yes"

"""

    # Format to: NONE
    blueprint_index_route = """\
from flask import render_template

from .. import bp


@bp.route("/", methods=["GET"])
def index():
    return render_template(bp.tmpl("index.html"))

"""

    # Format to: name
    blueprint_index_template = """\
<p>{name} index</p>
"""

    # Format to: name, static_url_path, url_prefix
    theme_config = """\
enabled = "yes"
static_folder = "static"
static_url_path = "{static_url_path}"
    """
