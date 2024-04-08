import importlib

from flask_imp.protocols import ImpConfigTemplate


def load_object(config: str) -> ImpConfigTemplate:
    import_split = config.split(".")

    config_module = importlib.import_module(".".join(import_split[:-1]))
    config = getattr(config_module, import_split[-1])

    if isinstance(config, ImpConfigTemplate):
        return config()

    raise ValueError(
        f"\nConfig object {config} is not an instance of ImpConfigTemplate\n"
    )
