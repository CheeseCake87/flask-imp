def extensions_init_full_py():
    return """\
from flask_imp import Imp
from flask_sqlalchemy import SQLAlchemy

imp = Imp()
db = SQLAlchemy()
"""


def extensions_init_slim_py():
    return """\
from flask_imp import Imp

imp = Imp()
"""
