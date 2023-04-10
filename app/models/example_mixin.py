from app import db
from flask_bigapp.orm import CrudMixin


class ExampleMixin(db.Model, CrudMixin):
    __id_field__ = "example_mixin_id"
    __session__ = db.session

    example_mixin_id = db.Column(db.Integer, primary_key=True)
    thing = db.Column(db.String(256), nullable=False)
