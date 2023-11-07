from app.extensions import db


class NestedTestModel(db.Model):
    __bind_key__ = "nested_test_database"

    nested_test_id = db.Column(db.Integer, primary_key=True)
    nested_test_name = db.Column(db.String(256), nullable=False)
