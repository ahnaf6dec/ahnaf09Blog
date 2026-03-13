from ..extensions import db

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_like = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))