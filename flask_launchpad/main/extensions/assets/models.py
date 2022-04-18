from . import db

sql_do = db.session


class FlUpload(db.Model):
    __tablename__ = "fl_upload"
    upload_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.Integer)
    url_for = db.Column(db.Integer)
