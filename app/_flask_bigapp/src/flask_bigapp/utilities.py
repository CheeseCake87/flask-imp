def contains_illegal_chars(name: str, exception: list = None) -> bool:
    _illegal_characters = ['%', '$', '£', ' ', '#', 'readme', '__', '.py']
    if exception is not None:
        for value in exception:
            _illegal_characters.remove(value)
    for char in _illegal_characters:
        if char in name:
            return True
    return False


def load_config(root_path: str) -> dict:
    from os import path
    from toml import load as toml_load

    config = {}
    if not path.isfile(f"{root_path}/config.toml"):
        raise ImportError(f"""
Config file is invalid, must be config.toml and be found in the root of the module. Importing from {root_path}
            """)

    config.update(toml_load(f"{root_path}/config.toml"))

    return config
