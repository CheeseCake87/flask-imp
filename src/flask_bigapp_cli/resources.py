class Resources:
    # Format to: NONE
    app_init = """\
from flask import Flask
from app.extensions import bigapp, db


def create_app():
    app = Flask(__name__)
    bigapp.init_app(app)
    #db.init_app(app)

    bigapp.import_global_collection()
    bigapp.import_blueprints("blueprints")

    #bigapp.import_models("models")

    return app\n\n"""

    extensions_init = """\
from flask_bigapp import BigApp
from flask_sqlalchemy import SQLAlchemy

bigapp = BigApp()
db = SQLAlchemy()
"""

    models_init = """\
from sqlalchemy import select, update, delete, insert
from sqlalchemy.orm import relationship
from app.extensions import db

__all__ = [
    "db",
    "select",
    "update",
    "delete",
    "insert",
    "relationship",
]

"""

    models_example_table = """\
from . import *


class ExampleUserTable(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    salt = db.Column(db.String(4), nullable=False)
    private_key = db.Column(db.String(256), nullable=False)
    disabled = db.Column(db.Boolean)

    @classmethod
    def get_by_id(cls, user_id):
        return db.session.execute(
            select(cls).filter_by(user_id=user_id).limit(1)
        ).scalar_one_or_none()

    @classmethod
    def create(cls, username, password, disabled):
        from flask_bigapp.auth import Auth

        salt = Auth.generate_salt()
        salt_pepper_password = Auth.hash_password(password, salt)
        private_key = Auth.generate_private_key(username)

        db.session.execute(
            insert(cls).values(
                username=username,
                password=salt_pepper_password,
                salt=salt,
                private_key=private_key,
                disabled=disabled,
            )
        )
        db.session.commit()

    @classmethod
    def update(cls, user_id, username, private_key, disabled):
        db.session.execute(
            update(cls).where(
                cls.user_id == user_id  # noqa
            ).values(
                username=username,
                private_key=private_key,
                disabled=disabled,
            )
        )
        db.session.commit()

    @classmethod
    def delete(cls, user_id):
        db.session.execute(
            delete(cls).where(
                cls.user_id == user_id  # noqa
            )
        )
        db.session.commit()

"""

    # Format to: NONE
    blueprint_init = """\
from flask_bigapp import Blueprint

bp = Blueprint(__name__)

bp.import_resource("routes")


@bp.before_app_request
def before_app_request():
    bp.init_session()

"""

    # Format to: name, url_prefix
    blueprint_config = """\
enabled = "yes"

[settings]
url_prefix = "/{url_prefix}"
#subdomain = ""
#url_defaults = {{}}
static_folder = "static"
template_folder = "templates"
static_url_path = "/static/{name}"

[session]
#{name}_session = "yes"

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
<img src="{{{{ url_for('{name}.static', filename='Flask-BigApp-Logo.svg') }}}}" alt="logo">
<p>{name} index</p>
"""

    global_cli_py = """\
def collection(app: object):
    from app.extensions import db
    from app.models.example__table import ExampleUserTable

    @app.cli.command("create-tables")
    def create_tables():
        db.create_all()

    @app.cli.command("get-example-user")
    def get_example_user():
        result = ExampleUserTable.get_by_id(1)
        if not result:
            print("User not found.")
            return
        print(
            f\"\"\"
            user_id: {result.user_id}
            username: {result.username}
            salt: {result.salt}
            password: {result.password}
            private_key: {result.private_key}
            disabled: {result.disabled}
            \"\"\"
        )

    @app.cli.command("add-example-user")
    def add_example_user():
        ExampleUserTable.add(
            username="admin",
            password="password",
            disabled=False,
        )

    @app.cli.command("add-example-user")
    def add_example_user():
        ExampleUserTable.add(
            username="admin",
            password="password",
            disabled=False,
        )

    @app.cli.command("update-example-user")
    def update_example_user():
        ExampleUserTable.update(
            user_id=1,
            username="admin-updated",
            private_key="private_key",
            disabled=False,
        )

    @app.cli.command("delete-example-user")
    def delete_example_user():
        ExampleUserTable.delete(
            user_id=1,
        )

"""

    # Format to: name
    global_context_processors_py = """\
def collection(app: object):
    @app.context_processor
    def example__utility_processor():
    \"""
    Usage:
    {{ format_price(100.33) }} -> $100.33
    \"""
\n
        def example__format_price(amount, currency='$'):
            return '{1}{0:.2f}'.format(amount, currency)
\n
        return dict(format_price=example__format_price)\n\n"""

    # Format to: name
    global_error_handlers_py = """\
def collection(app: object):
    from flask import render_template

    @app.errorhandler(400)
    def error_400(error):
        return render_template(
            "errors/400.html",
        ), 400

    @app.errorhandler(401)
    def error_401(error):
        return render_template(
            "errors/401.html",
        ), 401

    @app.errorhandler(403)
    def error_403(error):
        return render_template(
            "errors/403.html",
        ), 403

    @app.errorhandler(404)
    def error_404(error):
        return render_template(
            "errors/404.html",
        ), 404

    @app.errorhandler(405)
    def error_405(error):
        return render_template(
            "errors/405.html",
        ), 405

    @app.errorhandler(500)
    def error_500(error):
        return render_template(
            "errors/500.html",
        ), 500

"""

    # Format to: name
    global_filters_py = """\
def collection(app: object):
    @app.template_filter('example__num_to_month')
    def example__num_to_month(num: str) -> str:
        \"""
        Usage:
        {{ 1 | example__num_to_month }} -> January
        \"""
        if isinstance(num, int):
            num = str(num)

        months = {
            "1": "January",
            "2": "February",
            "3": "March",
            "4": "April",
            "5": "May",
            "6": "June",
            "7": "July",
            "8": "August",
            "9": "September",
            "10": "October",
            "11": "November",
            "12": "December",
        }

        if num in months:
            return months[num]
        return "Month not found"

"""

    # Format to: name
    global_routes_py = """\
def collection(app: object):
    from flask import render_template

    @app.route("/global")
    def index():
        return render_template(
            "index.html",
        )

"""

    # Format to: name
    global_static_main_css = """\
body, html {
    background-color: #c9c9c9;
}

"""

    # Format to: name
    global_static_logo_svg = """\
<?xml version="1.0" encoding="utf-8"?>
<svg viewBox="0 0 309 197" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect x="4.804" width="299.227" height="191.38" rx="8" ry="8" style="stroke: rgb(189, 189, 189); \
  paint-order: fill; fill: rgb(255, 255, 255);" y="2.928"/>
  <image width="309" height="197" xlink:href="data:image/png;charset=utf-8;base64,\
iVBORw0KGgoAAAANSUhEUgAAATUAAADFCAYAAAA1+mWpAAAC8n\
pUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHja7ZZbkusoDIbf\
WcUswZIQEsvBYKrODmb58ws7mY67T9VkzmugjNRcJKEPSKfj71\
8z/YVCpZSU1bzUUjaUXHPlBsW3s7TV0pZXu4ropdFrf+p6LWJ0\
Scw8//RySnr0Xwsekho0/WLI+zWwvw7UfNn3myG+IouIQh+XoX\
oZEj4H6DLQzm1tpbp93cJ+nPJaf6YBX1rKLey7zIbsDYUfYT6E\
ZEMrwmcAEh8naVAcLUnBxE0qdIWM9hEJEvJTnp6lIqIZoeYfJ7\
1QeWo3Wu2Ck+60Ml9T5Jbk8pQ/9ifS24A8/fNXz9kvjV/7RRZr\
RHTLfnxzDp9rz9hFywWpLtemHltcGubtcBGuPSG0shk+hQlbta\
I6TnXHURhb33bUTpUYuCZlGtRo0rFkp44QMx+JDQpzZ1mdLsaV\
O6iR5Kg02UBygCxLX9iz8DMWWm7r1tPy5vA8CFOZYIziXLxb07\
sL5oyrQBS5bLJyhZY5ko0wgly0mAYiNK+k6krwo95LcBUQ1Mhy\
XJGKxO6niV3p35dAFujAq5DnHSQblwGkCK4VwZCAAKiRKBXajN\
mIkEgHoIbQWTLvIECqPBAkZ8EtMnYO11hitKayMroT+vGYgYRK\
EQMb3DXAyllxfiw7zlBT0ayqRU1dq7YiJRfFs2glHsVmYjmZWj\
Ezt2rNxbOrFzd3r94qV8GjqbVUq15rbQ0+Gyw3rG6Y0NrOu+x5\
17SX3Xbf6946jk/PXXvp1r3X3gYPGXg/Rhk2fNTRDjpwlI586F\
EOO/yoR5s4alPSzFNnmTZ91tme1C6s3+ob1OiixotUTLQnNfSa\
PUxQPCcazACMUyYQt0CAA83BbHPKmYNcMNsq41YoI0gNZoOCGA\
jmg1gnPdglPokGuT/iliy/cOP/Sy4FujfJfef2E7URP0N9O69j\
3MJI6ia4fRg/vLG3+LH7JtPvBt6VH0MfQx9DH0MfQ//N0MSbHf\
98/wPeWgrfhGkfLAAAAYRpQ0NQSUNDIHByb2ZpbGUAAHicfZE9\
SMNQFIVPW6VFKhXsIOKQoTpZECviqFUoQoVQK7TqYPLSP2jSkK\
S4OAquBQd/FqsOLs66OrgKguAPiKOTk6KLlHhfUmgR44PL+zjv\
ncN99wH+ZpWpZs8EoGqWkUklhVx+VQi+IoQBqggSEjP1OVFMw3\
N93cPH97s4z/K+9+fqVwomA3wC8SzTDYt4g3h609I57xNHWVlS\
iM+Jxw1qkPiR67LLb5xLDvt5ZtTIZuaJo8RCqYvlLmZlQyWeIo\
4pqkb5/pzLCuctzmq1ztp98heGC9rKMtepRpDCIpYgQoCMOiqo\
wkKcdo0UExk6T3r4hx2/SC6ZXBUwciygBhWS4wf/g9+zNYuJST\
cpnAR6X2z7YxQI7gKthm1/H9t26wQIPANXWsdfawIzn6Q3Olrs\
CIhsAxfXHU3eAy53gKEnXTIkRwpQ+YtF4P2MvikPDN4CfWvu3N\
rnOH0AsjSr9A1wcAiMlSh73ePdoe65/XunPb8fY+VyoZ6/3CkA\
AA14aVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZX\
QgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6\
a2M5ZCI/Pgo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm\
1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA0LjQuMC1FeGl2MiI+\
CiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3\
JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogIDxyZGY6\
RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICB4bWxuczp4bX\
BNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIK\
ICAgIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3\
hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiCiAgICB4bWxu\
czpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS\
8iCiAgICB4bWxuczpHSU1QPSJodHRwOi8vd3d3LmdpbXAub3Jn\
L3htcC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYm\
UuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDov\
L25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgeG1wTU06RG9jdW\
1lbnRJRD0iZ2ltcDpkb2NpZDpnaW1wOjMyOGM3ZDY1LTRmNjct\
NDk1Yy1iOTQzLTU4OTRmYTA1ZDU3NCIKICAgeG1wTU06SW5zdG\
FuY2VJRD0ieG1wLmlpZDowOTU5NjJkZi1kNzUxLTRlZGMtODI3\
ZS1iZDJiYmYwOTlmNzYiCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW\
1lbnRJRD0ieG1wLmRpZDpiYjUxNDU5Yy1hMGFkLTQ2YWUtYmQ0\
OC1mNjM2NGI3Yjc2ODQiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG\
5nIgogICBHSU1QOkFQST0iMi4wIgogICBHSU1QOlBsYXRmb3Jt\
PSJMaW51eCIKICAgR0lNUDpUaW1lU3RhbXA9IjE2NjA2Mzk4NT\
QyNTYxMzAiCiAgIEdJTVA6VmVyc2lvbj0iMi4xMC4zMiIKICAg\
dGlmZjpPcmllbnRhdGlvbj0iMSIKICAgeG1wOkNyZWF0b3JUb2\
9sPSJHSU1QIDIuMTAiCiAgIHhtcDpNZXRhZGF0YURhdGU9IjIw\
MjI6MDg6MTZUMDk6NTA6NTQrMDE6MDAiCiAgIHhtcDpNb2RpZn\
lEYXRlPSIyMDIyOjA4OjE2VDA5OjUwOjU0KzAxOjAwIj4KICAg\
PHhtcE1NOkhpc3Rvcnk+CiAgICA8cmRmOlNlcT4KICAgICA8cm\
RmOmxpCiAgICAgIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiCiAgICAg\
IHN0RXZ0OmNoYW5nZWQ9Ii8iCiAgICAgIHN0RXZ0Omluc3Rhbm\
NlSUQ9InhtcC5paWQ6ZWNiODQ2YjItYjk5MC00OTQyLWFlOWMt\
MTI1ZWIyNTYxMzRhIgogICAgICBzdEV2dDpzb2Z0d2FyZUFnZW\
50PSJHaW1wIDIuMTAgKExpbnV4KSIKICAgICAgc3RFdnQ6d2hl\
bj0iMjAyMi0wOC0xNlQwOTo1MDo1NCswMTowMCIvPgogICAgPC\
9yZGY6U2VxPgogICA8L3htcE1NOkhpc3Rvcnk+CiAgPC9yZGY6\
RGVzY3JpcHRpb24+CiA8L3JkZjpSREY+CjwveDp4bXBtZXRhPg\
ogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg\
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgIC\
AgICAgICAgICAgICAgICAgICAgICAgCjw/eHBhY2tldCBlbmQ9\
InciPz529avHAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA\
AnAAAAJwEqCZFPAAAAB3RJTUUH5ggQCDI2QHneMQAAIABJREFU\
eNrtvXec3mWV/n9NL5nMpBfSEwi9o1SxoAiKDayrKCrq2lZ31V\
3Rta9l/bq2ta+Fta4LKlZERRBBWJASkB5CQkivk0yvvz/O+/zu\
M588M/NMCmn3eb2e18xTPv2+r/s6XcqSJUuWLFmyZMmSJUuWLF\
myZMmSJUuWLFmyZMmSJUuWLFmyZMmSJUuWLFmyZMmSJUuWLFmy\
ZMmSJUuWLFmyZMmSJUuWLFmyZMmSJUuWLFmyZMmSJUuWLFmyZM\
mSJUuWLFl2p1TkW5BljFIl6fWSLpC0WNIySc2Sfifp05K68i3K\
kiXL/iLVkv5H0qCkyyWN4/OFkm6U9KikI/JtypIly/4ibwTQvl\
Xiu6Ml9Un6Zr5NWbJk2V/kA4DahcN8/4ikDtTRLFn2mjqRJUu5\
UsnfGkl/lVQrqU5SA68pgFpnvlVZsmTZH2SSpHWS/k1SL6yt+P\
pjvk1ZsmTZn+QVMLG1w4Dah/MtypIly/4mPxsG0AYlvS7fnix7\
UyrzLciyE/JSSV8f5rtZ+fZkyZJlf5VvlWBq1ynFr2XJ8oRLzi\
jIsivyOpWOWbtPFq/2mKRWSeMlNUmql3lLV0r6s6TN+RZmyZJl\
X5IfaXjb2mivDlkmQpYsWbLsE/LaAkj9tPC+S9J/SfqEpP8dBt\
j+X76NWbJk2dtSIYtTG42J/VjSsYDfT2QpVMXfvCHfzixZsuxN\
aZH0i11QOYuvk/ItzZIly96SoyQ9tBsBbVDS92TOgyxZsmR5Qu\
UMSdt3Erj6Rvn+DkkvluWTZsmyy1KVb0GWMuRLMvvYzsgcSX+T\
FU+Ypx2LKMyUBfP+vaQzYYSTAcMtAF+WLFmy7FZ5hqT+nWBp/Y\
X9NEu6BJArZ/vNqKgvlsW5ZcmSJctukzt3Uv18Vol9VUi6dIz7\
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\
  ="/>
</svg>
"""

    # Format to: name
    global_static_main_js = """\
console.log('This log is from the file global/static/js/main.js')
"""

    # Format to: name
    page_400 = """\
<!doctype html>
<html lang="en">

<head>
    <title>400 Bad Request</title>
</head>

<body>
<p>It's not us, it's you.</p>
</body>
</html>

"""

    # Format to: name
    page_401 = """\
<!doctype html>
<html lang="en">

<head>
    <title>401 Unauthorized</title>
</head>

<body>
<p>You lack valid authentication credentials for the requested resource</p>
</body>
</html>

"""

    # Format to: name
    page_403 = """\
<!doctype html>
<html lang="en">

<head>
    <title>403 Forbidden</title>
</head>

<body>
<p>Access forbidden!</p>
</body>
</html>

"""

    # Format to: name
    page_404 = """\
<!doctype html>
<html lang="en">

<head>
    <title>404 Page Not Found</title>
</head>

<body>
<p>No route associated with the URL</p>
</body>
</html>

"""

    # Format to: name
    page_405 = """\
<!doctype html>
<html lang="en">

<head>
    <title>405 Method Not Allowed</title>
</head>

<body>
<p>Should of GET when you POST, or POST when you GET</p>
</body>
</html>

"""

    # Format to: name
    page_500 = """\
<!doctype html>
<html lang="en">

<head>
    <title>500 Server Error!</title>
</head>

<body>
<p>There has been a server error!</p>
</body>
</html>

"""

    # Format to: name
    extends_main = """\
<!doctype html>

<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %} {% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</head>

<body>
<img src="{{ url_for('static', filename='img/Flask-BigApp-Logo.svg') }}" alt="logo">
{% include "includes/menu.html" %}
{% block global %}

{% endblock %}
{% include "includes/footer.html" %}
</body>

</html>
"""

    # Format to: name
    includes_footer = """\
<p>footer</p>
"""

    # Format to: name
    includes_header = """\
<p>header</p>
"""

    # Format to: name
    index_html = """\
{% extends 'extends/main.html' %}


{% block global %}

    <p>This is the template file located in app/global/templates</p>

{% endblock %}
"""
