from ..extensions import db

class Contact(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120))

    message = db.Column(db.Text)