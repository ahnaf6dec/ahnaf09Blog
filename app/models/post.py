from ..extensions import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    comments = db.relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
        lazy=True
    )

    likes = db.relationship("Like", backref="post", lazy=True)
    bookmarks = db.relationship("Bookmark", backref="post", lazy=True)

    tags = db.relationship(
        "Tag",
        secondary="post_tags",
        lazy="subquery",
        backref=db.backref("posts", lazy=True)
    )