## Version x.x.x

---

Unreleased

- ...

## Version 5.7.0

---

Released 2025-02-10

- add new method: `FlaskConfig.as_object`
- refactored _flask_config.py

## Version 5.6.0

---

Released 2025-02-04

- New method added to register ImpBlueprints
- Addition of two new decorators @checkpoint and @api_checkpoint these will eventually
  replace login_check, api_login_check and permission_check
- remove old reminder to check old settings file
- update classifiers in pyproject.toml

## Version 5.5.1

---

Released 2024-12-04

- switched logo for emoji
- fixed `initial-scale` value in generated templates
- updated example app

## Version 5.5.0

---

Released 2024-11-21

- updated project structure.
- docs now using sphinx + readthedocs.
- the start of the changes.md file.
- changes to the order of arguments in database configs
- argument 'name' changed to 'database_name' in configs
- addition of abort_status and fail_status args in security decorators
