import importlib
import multiprocessing
import os
import subprocess
from abc import ABC

import gunicorn.app.base

from app import create_app


def init_log_files(clear, a_log: str = "sgi.access.log", e_log: str = "sgi.error.log") -> tuple:
    if not os.path.isfile(a_log) or clear:
        with open(a_log, "w") as a:
            a.write("")
    if not os.path.isfile(e_log) or clear:
        with open(e_log, "w") as e:
            e.write("")
    return a_log, e_log


def package_check(package) -> str:
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.call(['venv/bin/python', '-m', 'pip', 'install', package])
    return package


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class SGIapp(gunicorn.app.base.BaseApplication, ABC):
    def __init__(self, application, options):
        self.application = application
        self.options = options or dict()
        super().__init__()

    def load_config(self):
        _config = {key: value for key, value in self.options.items()
                   if key in self.cfg.settings and value is not None}
        for key, value in _config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':

    FRAMEWORK = os.environ.get('FRAMEWORK', 'flask')
    ENV = os.environ.get('ENV', 'development')
    BIND = os.environ.get('BIND', "127.0.0.1:5000")
    WORKERS = os.environ.get('WORKERS', number_of_workers())
    CLEAR_LOG = os.environ.get('CLEAR_LOG', False)

    sgi_config = {
        'bind': BIND,
        'workers': WORKERS,
    }

    access_log, error_log = init_log_files(CLEAR_LOG)

    if FRAMEWORK == 'flask':
        sgi_config['worker_class'] = package_check('gevent')

    if ENV == "production":
        os.environ['FLASK_ENV'] = 'production'
        sgi_config.update({
            'loglevel': 'warning',
            'accesslog': access_log,
            'errorlog': error_log
        })
        SGIapp(create_app(), sgi_config).run()

    if ENV == "production_testing":
        sgi_config.update({
            'reload': True,
            'loglevel': 'debug',
        })
        SGIapp(create_app(), sgi_config).run()

    if ENV == "development":
        app = create_app()
        app.run()
else:
    app = create_app()
    app.run()
