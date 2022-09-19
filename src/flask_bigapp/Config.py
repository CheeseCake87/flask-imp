import os
import re
from typing import TextIO, Dict, Any, Union
from flask import Flask
from flask import current_app
from toml import load
from .Resources import Resources


class Config:
    app: Flask
    config_file: Union[str, TextIO, None]
    temp_config: Dict
    config: Dict
    _pattern = re.compile(r'<(.*?)>')

    def __init__(self, app: Flask, config_file: Union[str, TextIO, None]):
        self.app = app
        self.config_file = config_file
        self.temp_config = self.load_config()

    def load_config(self) -> dict:
        with self.app.app_context():
            if os.path.isfile(f"{current_app.root_path}/{self.config_file}"):
                return load(f"{current_app.root_path}/{self.config_file}")

            if os.path.isfile(f"{current_app.root_path}/default.config.toml"):
                return load(f"{current_app.root_path}/default.config.toml")

            with open(f"{current_app.root_path}/default.config.toml", mode="w") as dc:
                dc.write(Resources.default_config)
            return load(f"{current_app.root_path}/default.config.toml")

    def if_env_replace(self, value: str) -> str:
        if isinstance(value, str):
            if re.match(self._pattern, value):
                env_var = re.findall(self._pattern, value)[0]
                return os.environ.get(env_var, "ENV_KEY_NOT_FOUND")
        return value

    def set_app_config(self) -> None:
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
        config_rebuild: dict = dict()

        if self.temp_config.get("smtp", False):
            config_smtp = self.temp_config['smtp']

            for key, value in config_smtp.items():
                this_key = self.if_env_replace(key)
                config_rebuild.update({this_key: Dict[str, Any]})

                for ikey, ivalue in value.items():
                    config_rebuild[this_key].update({ikey: self.if_env_replace(ivalue)})

            # Delete the SMTP section from the config to stop it from getting in the way further on
            del self.temp_config["smtp"]
            return config_rebuild

        # Return the config
        return {}

    def build_database_uri(self, dbc: dict, root_path: str) -> str:
        db_type = self.if_env_replace(dbc.get('type', 'null'))

        if db_type == 'sqlite':
            if dbc.get('database_name', None) is None:
                raise ImportError("sqlite database config detected, but no database_name defined")
            if dbc.get('location', None) is None:
                return f"{dbc.get('type')}:////{root_path}/{dbc['database_name']}.sqlite"
            if not os.path.isdir(f"{root_path}/{dbc.get('location', 'db')}"):
                os.mkdir(f"{root_path}/{dbc.get('location', 'db')}")

            return f"{db_type}:////{root_path}/{dbc.get('location', 'db')}/{dbc['database_name']}.sqlite"

        accepted_types = ['postgresql', 'mysql', 'oracle']

        if db_type in accepted_types:
            if dbc.get('location', None) is None:
                raise ImportError(f"{dbc.get('type', None)} database config detected, but no location defined")
            if dbc.get('database_name', None) is None:
                raise ImportError(f"{dbc.get('type', None)} database config detected, but no database_name defined")
            if dbc.get('username', None) is None:
                raise ImportError(f"{dbc.get('type', None)} database config detected, but no username defined")
            if dbc.get('password', None) is None:
                raise ImportError(f"{dbc.get('type', None)} database config detected, but no password defined")

            location = self.if_env_replace(dbc.get('location', None))
            database_name = self.if_env_replace(dbc.get('database_name', None))
            username = self.if_env_replace(dbc.get('username', None))
            password = self.if_env_replace(dbc.get('password', None))

            return f"{db_type}://{username}:{password}@{location}/{database_name}"

        raise ValueError(f"Unknown database type: {db_type} - valid options are: 'sqlite', 'postgresql', 'mysql', 'oracle'")

    def set_database_config(self):
        """

        """
        if self.temp_config.get("database", False):
            with self.app.app_context():
                config_database = self.temp_config["database"]
                current_app.config["SQLALCHEMY_BINDS"] = dict()

                if config_database.get("main", False):
                    main_database = config_database["main"]
                    main_database_enabled = main_database.get("enabled", False)
                    if main_database_enabled:
                        current_app.config["SQLALCHEMY_DATABASE_URI"] = self.build_database_uri(
                            main_database, current_app.root_path
                        )

                    # Remove the main key away, so we can loop over the rest
                    del config_database["main"]

                for key, value in config_database.items():
                    current_app.config["SQLALCHEMY_BINDS"].update(
                        {self.if_env_replace(key): self.build_database_uri(value, current_app.root_path)}
                    )
