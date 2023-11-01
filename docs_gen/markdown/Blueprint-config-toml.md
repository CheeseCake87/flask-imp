```
Menu = Blueprint/config.toml
Title = The Flask-Imp Blueprint Config File
```

The Flask-Imp Blueprint will load configuration from a `config.toml` file, which is located in the same directory as the
`__init__.py` file.

File: `config.toml`

```toml
enabled = "yes"

[settings]
url_prefix = ""
subdomain = ""
url_defaults = { }
static_folder = ""
template_folder = ""
static_url_path = ""
#root_path = ""
#cli_group = ""

[session]
var = ""
```

This config reflects the args that are passed to a regular Flask Blueprint class, the addition of the ability to
enable/disable the Blueprint, and set session variables.

For more information about the args of a regular Flask Blueprint see:
[Flask docs (Blueprint)](https://flask.palletsprojects.com/en/3.0.x/api/#flask.Blueprint)

##### Example of advance use case for blueprint config files:

```text
testing_blueprint/
├── routes/
│   └── index.py
├── static/
│   └── ...
├── templates/
│   └── www/
│       └── index.html
├── __init__.py
├── pro_config.py
└── dev_config.toml
```

```python
from app import app
from flask_imp import Blueprint

bp = Blueprint(
    __name__, 
    config_file="dev_config.toml" if app.config["DEBUG"] else "pro_config.py"
)

bp.import_resources("routes")


@bp.before_app_request
def before_app_request():
    bp.init_session()
```

File: `pro_config.py`

```toml
enabled = "no"

[settings]
#url_prefix = ""
#subdomain = ""
#url_defaults = { }
#static_folder = ""
#template_folder = ""
#static_url_path = ""
#root_path = ""
#cli_group = ""

[session]
#var = ""
```

File: `dev_config.py`

```toml
enabled = "yes"

[settings]
url_prefix = "/testing"
#subdomain = ""
#url_defaults = { }
static_folder = "static"
template_folder = "templates"
#static_url_path = ""
#root_path = ""
#cli_group = ""

[session]
#var = ""
```

In the example above, the `testing_blueprint` will only be enabled if the Flask app is running in debug mode.