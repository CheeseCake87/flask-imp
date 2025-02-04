# Flask-Imp 🧚

![tests](https://github.com/CheeseCake87/flask-imp/actions/workflows/tests.yml/badge.svg)
[![PyPI version](https://img.shields.io/pypi/v/flask-imp)](https://pypi.org/project/flask-imp/)
[![License](https://img.shields.io/github/license/CheeseCake87/flask-imp)](https://raw.githubusercontent.com/CheeseCake87/flask-imp/master/LICENSE)
![black](https://img.shields.io/badge/code%20style-black-000000.svg)

## What is Flask-Imp?

Flask-Imp's main purpose is to help simplify the importing of blueprints, resources, and
models. It has a few extra
features built in to help with securing pages and password authentication.

```bash
pip install flask-imp
```



```{toctree}
:maxdepth: 1

getting-started.md
Imp/Imp-Introduction.md
ImpBlueprint/ImpBlueprint-Introduction.md
```

```{toctree}
:caption: CLI Commands
:maxdepth: 1

CLI_Commands/CLI_Commands-flask-imp_init.md
CLI_Commands/CLI_Commands-flask-imp_blueprint.md
```

```{toctree}
:caption: config
:maxdepth: 1

Config/flask_imp_config-flaskconfig.md
Config/flask_imp_config-impconfig.md
Config/flask_imp_config-impblueprintconfig.md
Config/flask_imp_config-databaseconfig.md
Config/flask_imp_config-sqldatabaseconfig.md
Config/flask_imp_config-sqlitedatabaseconfig.md
```

```{toctree}
:caption: Imp
:maxdepth: 1

Imp/Imp-init_app-init.md
Imp/Imp-init_session.md
Imp/Imp-import_app_resources.md
Imp/Imp-import_blueprint.md
Imp/Imp-import_blueprints.md
Imp/Imp-Imp-register_imp_blueprint.md
Imp/Imp-import_models.md
Imp/Imp-model.md
```

```{toctree}
:caption: ImpBlueprint
:maxdepth: 1

ImpBlueprint/ImpBlueprint-init.md
ImpBlueprint/ImpBlueprint-import_resources.md
ImpBlueprint/ImpBlueprint-import_nested_blueprint.md
ImpBlueprint/ImpBlueprint-import_nested_blueprints.md
ImpBlueprint/ImpBlueprint-import_models.md
ImpBlueprint/ImpBlueprint-tmpl.md
```

```{toctree}
:caption: auth
:maxdepth: 1

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
:maxdepth: 1

Security/flask_imp_security-checkpoint.md
Security/flask_imp_security-api_checkpoint.md
Security/flask_imp_security-include_csrf.md
Security/flask_imp_security-login_check.md
Security/flask_imp_security-api_login_check.md
Security/flask_imp_security-permission_check.md
Security/flask_imp_security-pass_function_check.md
```

```{toctree}
:caption: API

API/index
```
