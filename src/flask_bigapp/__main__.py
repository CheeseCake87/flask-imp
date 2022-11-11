import sys
from pathlib import Path


def create_blueprint(path, name):
    Path.mkdir(path / name)
    Path.mkdir(path / name / "routes")
    Path.mkdir(path / name / "templates")
    Path.mkdir(path / name / "templates" / name)

    with open(path / name / "__init__.py", "w") as f:
        f.write("""\
from flask_bigapp import Blueprint

bp = Blueprint(__name__)

bp.import_routes("routes")


@bp.before_app_request
def before_app_request():
    bp.init_session()


@bp.after_app_request
def after_app_request(response):
    return response

""")

    with open(path / name / "config.toml", "w") as f:
        f.write(f"""\
enabled = "yes"

[settings]
url_prefix = "/{name}"
template_folder = "templates"
static_folder = "static"
#static_url_path = "/{name}/static"

[session]
{name}_session = "yes"

""")

    with open(path / name / "routes" / "index.py", "w") as f:
        f.write("""\
from flask import render_template

from .. import bp


@bp.route("/", methods=["GET"])
def index():
    return render_template(bp.tmpl("index.html"))
""")

    with open(path / name / "templates" / name / "index.html", "w") as f:
        f.write(f"""\
<p>{name} index</p>
""")


if "--add-bp-in" in sys.argv:
    put_bp_in = None
    called = None

    try:
        put_bp_in = sys.argv[sys.argv.index("--add-bp-in") + 1]
    except IndexError:
        print("No path provided for --add-bp-in")
        exit()

    # """if string starts with a / or \, remove it"""
    if put_bp_in.startswith("/") or put_bp_in.startswith("\\"):
        put_bp_in = put_bp_in[1:]

    # """if string ends with a / or \, remove it"""
    if put_bp_in.endswith("/") or put_bp_in.endswith("\\"):
        put_bp_in = put_bp_in[:-1]

    add_to = Path(Path.cwd() / put_bp_in)

    if not add_to.exists():
        print(f"Path {add_to} does not exist")
        exit()

    if "--called" in sys.argv:
        try:
            called = sys.argv[sys.argv.index("--called") + 1]
        except IndexError:
            print('No name provided for the blueprint, should be --called "<name>"')
            exit()
        create_blueprint(add_to, called)
    else:
        print("You must specify a name for the blueprint")
        exit()
