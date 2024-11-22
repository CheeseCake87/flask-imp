# Flask-Imp

![tests](https://github.com/CheeseCake87/flask-imp/actions/workflows/tests.yml/badge.svg)
[![PyPI version](https://img.shields.io/pypi/v/flask-imp)](https://pypi.org/project/flask-imp/)
[![License](https://img.shields.io/github/license/CheeseCake87/flask-imp)](https://raw.githubusercontent.com/CheeseCake87/flask-imp/master/LICENSE)
![Downloads](https://static.pepy.tech/badge/flask-imp)
![black](https://img.shields.io/badge/code%20style-black-000000.svg)

## What is Flask-Imp?

Flask-Imp's main purpose is to help simplify the importing of blueprints, resources, and models. It has a few extra
features built in to help with securing pages and password authentication.

### Install Flask-Imp

```bash
pip install flask-imp
```

### Generate a Flask app

```bash
flask-imp init
```

```{toctree}
:hidden:

getting-started.md
```

```{toctree}
:hidden:

API/index
```

```{toctree}
:caption: CLI Commands
:hidden:

CLI Commands/CLI Commands-flask-imp init.md
CLI Commands/CLI Commands-flask-imp blueprint.md
```

```{toctree}
:caption: Imp
:hidden:

Imp/Imp-Introduction.md
Imp/Imp-init_app-init.md
Imp/Imp-init_session.md
Imp/Imp-import_app_resources.md
Imp/Imp-import_blueprint.md
Imp/Imp-import_blueprints.md
Imp/Imp-import_models.md
Imp/Imp-model.md
```

```{toctree}
:caption: ImpBlueprint
:hidden:

ImpBlueprint/ImpBlueprint-Introduction.md
ImpBlueprint/ImpBlueprint-init.md
ImpBlueprint/ImpBlueprint-import_resources.md
ImpBlueprint/ImpBlueprint-import_nested_blueprint.md
ImpBlueprint/ImpBlueprint-import_nested_blueprints.md
ImpBlueprint/ImpBlueprint-import_models.md
ImpBlueprint/ImpBlueprint-tmpl.md
```

```{toctree}
:caption: config
:hidden:

Configs/flask_imp_config-flaskconfig.md
Configs/flask_imp_config-impconfig.md
Configs/flask_imp_config-impblueprintconfig.md
Configs/flask_imp_config-databaseconfig.md
Configs/flask_imp_config-sqldatabaseconfig.md
Configs/flask_imp_config-sqlitedatabaseconfig.md
```

```{toctree}
:caption: auth
:hidden:

Auth/flask_imp_auth-authenticate_password.md
Auth/flask_imp_auth-encrypt_password.md
Auth/flask_imp_auth-generate_alphanumeric_validator.md
Auth/flask_imp_auth-generate_csrf_token.md
Auth/flask_imp_auth-generate_email_validator.md
Auth/flask_imp_auth-generate_numeric_validator.md
Auth/flask_imp_auth-generate_password.md
Auth/flask_imp_auth-generate_private_key.md
Auth/flask_imp_auth-generate_salt.md
Auth/flask_imp_auth-is_email_address_valid.md
Auth/flask_imp_auth-is_username_valid.md
```

```{toctree}
:caption: security
:hidden:

Security/flask_imp_security-include_csrf.md
Security/flask_imp_security-login_check.md
Security/flask_imp_security-api_login_check.md
Security/flask_imp_security-permission_check.md
Security/flask_imp_security-pass_function_check.md
```

