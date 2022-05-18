from .. import db


class ApiExample(db.Model):
    __tablename__ = "api_example"
    api_example_id = db.Column(db.Integer, primary_key=True)
