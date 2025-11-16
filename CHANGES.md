## Version x.x.x

---

Unreleased

- x

## Version 6.0.3

---

Released 2025-11-16

- fix to 'SessionCheckpoint' value checker

## Version 6.0.2

---

Released 2025-10-21

- further fixes to prevent the import of hidden and dunder files and folders

## Version 6.0.1

---

Released 2025-10-21

- fix to prevent hidden files and folders being imported, this is files that start with
  `.` for example `.cli.py` and folders that start with `.` for example `.DS_Store`

## Version 6.0.0

---

Released 2025-10-16

- beta-3 + beta-2 + beta-1

## Version 6.0.0-beta.3

---

Released 2025-10-16

- Replaced `import_app_resources` with
  `import_resources` and made it more scoped towards
  importing and setting up factories. Static and template folder settings moved back to
  being set in the Flask object creation.
- factories are now mandatory when using `import_resources`
- Update CLI init command to reflect method replacement.
- Update Docs to reflect method `import_app_resources` replacement.
- Actually return `ImpBlueprint.as_flask_blueprint` as a Flask Blueprint
- replace `pass_function_check` with `checkpoint_callable`
- add `APIKeyCheckpoint`
- refactor all checkpoint args
- add `utilities.lazy_url_for`
- add `utilities.lazy_session_get`
- update overall docs

## Version 6.0.0-beta.2

---

Released 2025-05-27

- bug fixes
- move checkpoints to package

## Version 6.0.0-beta.1

---

Released 2025-05-27

- Simplify `flask_imp.security.checkpoint` decorator by adding checkpoint types.

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
