from .....extensions import db


class NestedTestModel(db.Model):
    nested_test_id = db.Column(db.Integer, primary_key=True)
    nested_test_name = db.Column(db.String(256), nullable=False)
