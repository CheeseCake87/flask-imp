# Flask-Imp 🧚

![tests](https://github.com/CheeseCake87/flask-imp/actions/workflows/tests.yml/badge.svg)
[![PyPI version](https://img.shields.io/pypi/v/flask-imp)](https://pypi.org/project/flask-imp/)
[![License](https://img.shields.io/github/license/CheeseCake87/flask-imp)](https://raw.githubusercontent.com/CheeseCake87/flask-imp/master/LICENSE)

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
:caption: Config
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
Imp/Imp-import_resources.md
Imp/Imp-import_blueprint.md
Imp/Imp-import_blueprints.md
Imp/Imp-register_imp_blueprint.md
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
:caption: Security
:maxdepth: 1

Security/flask_imp_security-checkpoint.md
Security/flask_imp_security-checkpoint_callable.md
Security/flask_imp_security-include_csrf.md
```

```{toctree}
:caption: Security Checkpoints
:maxdepth: 1

SecurityCheckpoints/flask_imp_security-apikeycheckpoint.md
SecurityCheckpoints/flask_imp_security-bearercheckpoint.md
SecurityCheckpoints/flask_imp_security-sessioncheckpoint.md
SecurityCheckpoints/flask_imp_security-createacheckpoint.md
```

```{toctree}
:caption: Auth
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
:caption: Utilities
:maxdepth: 1

Utilities/flask_imp_utilities-lazy_url_for.md
Utilities/flask_imp_utilities-lazy_session_get.md
```

```{toctree}
:caption: API

API/index
```
