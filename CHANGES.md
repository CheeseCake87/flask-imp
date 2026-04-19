## Version x.x.x

Unreleased

## Version 6.3.0

Released 2026-04-19

- fix missing `raise` on `scope_import is None` check in `process_folder_file_scope`
- use context manager for `multiprocessing.Pool` in `authenticate_password` to stop worker leak
- fix `disable_default_fail` semantics on `checkpoint_callable` — default now aborts with `fail_status`
  when no fail handler is set (previously it silently called the protected view)
- use `secrets.compare_digest` for bearer token comparison in `BearerCheckpoint`
- mix `secrets.token_hex` entropy into `generate_csrf_token` output
- `ImpBlueprint.import_resources` now routes through `cast_to_import_str`, fixing import paths for
  nested resource folders
- preserve order when deduping scoped import results (`dict.fromkeys` instead of `set`)
- URL-encode username/password when building database URIs to avoid breakage on special characters
- chain `ImportError` re-raises with `from e` to preserve the original traceback
- add testing for checkpoints

## Version 6.2.0

Released 2026-04-14

- auth.generate_private_key
- auth.authenticate_password
- auth.encrypt_password

The function argument `encryption_level` has been changed to `algorithm` and has a new type of **Literal**

This was done to allow for more algorithms to be added in the future.

## Version 6.1.5

Released 2026-02-22

- bugfix

## Version 6.1.4 - YANKED

Released 2026-02-21

- add disable_default_fail option to checkpoints

## Version 6.1.3

Released 2026-02-21

- adjust fail_response to accept a callable to avoid out of context error

## Version 6.1.2

Released 2026-02-21

- switch checkpoint type checking to protocol matching

## Version 6.1.1

Released 2026-02-21

- checkpoint bug fix, docs fix, bump version

## Version 6.1.0

Released 2026-02-21

- add the ability to pass a Flask Response object as a fail method on a checkpoint.

## Version 6.0.3

Released 2025-11-16

- fix to 'SessionCheckpoint' value checker

## Version 6.0.2

Released 2025-10-21

- further fixes to prevent the import of hidden and dunder files and folders

## Version 6.0.1

Released 2025-10-21

- fix to prevent hidden files and folders being imported, this is files that start with
  `.` for example `.cli.py` and folders that start with `.` for example `.DS_Store`

## Version 6.0.0

Released 2025-10-16

- beta-3 + beta-2 + beta-1

## Version 6.0.0-beta.3

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

Released 2025-05-27

- bug fixes
- move checkpoints to package

## Version 6.0.0-beta.1

Released 2025-05-27

- Simplify `flask_imp.security.checkpoint` decorator by adding checkpoint types.

## Version 5.7.0

Released 2025-02-10

- add new method: `FlaskConfig.as_object`
- refactored _flask_config.py

## Version 5.6.0

Released 2025-02-04

- New method added to register ImpBlueprints
- Addition of two new decorators @checkpoint and @api_checkpoint these will eventually
  replace login_check, api_login_check and permission_check
- remove old reminder to check old settings file
- update classifiers in pyproject.toml

## Version 5.5.1

Released 2024-12-04

- switched logo for emoji
- fixed `initial-scale` value in generated templates
- updated example app

## Version 5.5.0

Released 2024-11-21

- updated project structure.
- docs now using sphinx + readthedocs.
- the start of the changes.md file.
- changes to the order of arguments in database configs
- argument 'name' changed to 'database_name' in configs
- addition of abort_status and fail_status args in security decorators
