from app.extensions import db


class TestModel(db.Model):
    __bind_key__ = "tests_database"

    test_id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(256), nullable=False)
