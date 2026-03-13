from ..extensions import db

class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avatar_url = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(500), nullable=False)
    social_link = db.Column(db.String(250), nullable=True)