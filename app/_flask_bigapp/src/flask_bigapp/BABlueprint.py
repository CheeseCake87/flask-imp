class BABlueprint:
    """
    Class that handles Blueprints from within the Blueprint __init__ file
    """
    module = None
    import_from = None
    root_path = None
    config_file = None
    config = None
    session = {}

    def __init__(self):
        from inspect import stack

        caller = stack()[1]
        split_module_folder = caller.filename.split("/")[:-1]
        self.root_path = "/".join(split_module_folder)
        self.import_from = caller.filename.split("/")[-3:-2][0]
        self.name = caller.filename.split("/")[-2:-1][0]

    def register(self):
        from flask import Blueprint
        from .utilities import load_config

        self.config = load_config(self.root_path)

        try:
            c_init = self.config["init"]
            c_settings = self.config["settings"]
            c_blueprint = self.config["blueprint"]
        except KeyError:
            raise ImportError(f"{self.import_from} INIT and SETTINGS sections missing from config file.")

        if c_init["enabled"]:
            if c_settings["type"] == "api":
                new_url = f"/{self.import_from}{c_blueprint['url_prefix']}"
                c_settings['url_prefix'] = new_url

        if "session" in self.config:
            s = self.config["session"]
            for key, value in s.items():
                self.session[key] = value

        bp_name, bp_import_name = self.name, self.name

        if "name" in c_blueprint:
            bp_name = c_blueprint["name"]
            del c_blueprint["name"]

        if "import_name" in c_blueprint:
            bp_import_name = c_blueprint["import_name"]
            del c_blueprint["import_name"]

        if "template_folder" in c_blueprint:
            c_blueprint["template_folder"] = f"{self.root_path}/{c_blueprint['template_folder']}"

        if "static_folder" in c_blueprint:
            c_blueprint["static_folder"] = f"{self.root_path}/{c_blueprint['static_folder']}"

        return Blueprint(bp_name, bp_import_name, **c_blueprint)

    def import_routes(self, folder: str = "routes"):
        from os import listdir
        from importlib import import_module
        from flask import current_app
        from .utilities import contains_illegal_chars

        routes_raw, routes_clean = listdir(f"{self.root_path}/{folder}"), []
        for route in routes_raw:
            if contains_illegal_chars(route, exception=[".py"]):
                continue
            routes_clean.append(route.replace(".py", ""))

        for route in routes_clean:
            try:
                import_module(f"{current_app.name}.{self.import_from}.{self.name}.{folder}.{route}")
            except ImportError as e:
                print(f"""
Error when importing {self.import_from} - {self.name} - {route}: 
{e}
                """)
                continue

