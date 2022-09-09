import os
import re


class Config:
    app = None
    config_file = None
    temp_config = None
    config = None
    pattern = re.compile(r'<(.*?)>')

    def __init__(self, app, config_file):
        self.app = app
        self.config_file = config_file
        self.load_config(config_file)

    def load_config(self, config_file):
        from flask import current_app
        from toml import load
        import os

        if config_file is None:
            self.config_file = "config.toml"

        with self.app.app_context():
            if not os.path.isfile(f"{current_app.root_path}/{self.config_file}"):
                raise ImportError(
                    """App has no valid config file, must be like config.toml and be in the root of the app.""")
            current_app.config["SQLALCHEMY_BINDS"] = dict()

            self.temp_config = load(f"{current_app.root_path}/{self.config_file}")

    def if_env_replace(self, value):
        if isinstance(value, str):
            if re.match(self.pattern, value):
                env_var = re.findall(self.pattern, value)[0]
                return os.environ.get(env_var, "ENV_KEY_NOT_FOUND")
        return value

    def set_app_config(self) -> None:
        from flask import current_app

        if self.temp_config.get('flask', False):
            # load the temp_config into a local param to the method
            config_app = self.temp_config['flask']

            # Extract the static and template folder values from the config
            static_folder = config_app.get('static_folder', False)
            template_folder = config_app.get('template_folder', False)

            # With context set the config values to the app
            with self.app.app_context():
                if static_folder:
                    # Set the static folder
                    current_app.static_folder = f"{current_app.root_path}/{self.if_env_replace(static_folder)}"
                    # Delete the key to remove if from the loop below
                    del config_app["static_folder"]

                if template_folder:
                    # Set the template folder
                    current_app.template_folder = f"{current_app.root_path}/{self.if_env_replace(template_folder)}"
                    # Delete the key to remove if from the loop below
                    del config_app["template_folder"]

                # Loop over the rest of the app section and set it into the current apps config
                for key, value in config_app.items():
                    current_app.config[key.upper()] = self.if_env_replace(value)

            # Delete the flask section from the temp config
            del self.temp_config["flask"]
            return

        # Raise error as the app section was not found
        raise ImportError("Config file is missing the 'flask' section")

    def set_smtp_config(self) -> dict:
        """
        Outputs the smtp config to be added to bigapp config

        Is able to support environment variables. Replace the values of the config file
        with the environment variable you plan to pass in, e.g. <EMAIL_PASSWORD>
        This will be replaced by the os.environment variable value
        """

        if self.temp_config.get("smtp", False):
            config_smtp = self.temp_config['smtp']
            config_rebuild = dict()

            for key, value in config_smtp.items():
                this_key = self.if_env_replace(key)
                config_rebuild.update({this_key: {}})

                for ikey, ivalue in value.items():
                    config_rebuild[this_key][ikey] = self.if_env_replace(ivalue)

            # Delete the SMTP section from the config to stop it from getting in the way further on
            del self.temp_config["smtp"]

            # Return the config
            return config_rebuild

        return dict()

    def set_database_config(self):
        from flask import current_app

        def build_uri(dbc: dict = None, root_path: str = None):
            db_type = self.if_env_replace(dbc.get('type', None))

            if db_type == 'sqlite':
                if dbc.get('database_name', None) is None:
                    raise ImportError("sqlite  database config detected, but no database_name defined")
                return f"{dbc.get('type')}:////{root_path}/{dbc.get('database_name', None)}.sqlite"

            accepted_types = ['postgresql', 'mysql', 'oracle']

            if db_type in accepted_types:
                if dbc.get('server', None) is None:
                    raise ImportError(f"{dbc.get('type', None)} database config detected, but no server defined")
                if dbc.get('database_name', None) is None:
                    raise ImportError(f"{dbc.get('type', None)} database config detected, but no database_name defined")
                if dbc.get('username', None) is None:
                    raise ImportError(f"{dbc.get('type', None)} database config detected, but no username defined")
                if dbc.get('password', None) is None:
                    raise ImportError(f"{dbc.get('type', None)} database config detected, but no password defined")

                server = self.if_env_replace(dbc.get('server', None))
                database_name = self.if_env_replace(dbc.get('database_name', None))
                username = self.if_env_replace(dbc.get('username', None))
                password = self.if_env_replace(dbc.get('password', None))

                return f"{self.if_env_replace(dbc.get('type'))}://{username}:{password}@{server}/{database_name}"

        if self.temp_config.get("database", False):
            config_database = self.temp_config["database"]
            if config_database.get("main", False):
                main_database = config_database["main"]
                main_database_enabled = main_database.get("enabled", False)
                with self.app.app_context():
                    if main_database_enabled:
                        current_app.config["SQLALCHEMY_DATABASE_URI"] = build_uri(main_database, current_app.root_path)

                # Remove the main key away, so we can loop over the rest
                del config_database["main"]

            for key, value in config_database.items():
                current_app.config["SQLALCHEMY_BINDS"].update({self.if_env_replace(key): build_uri(value, current_app.root_path)})
