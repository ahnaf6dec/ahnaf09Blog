from ..extensions import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    # reply system
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"), nullable=True)

    # soft-delete flag
    is_deleted = db.Column(db.Boolean, default=False)

    # relationships
    user = db.relationship("User", back_populates="comments")
    post = db.relationship("Post", back_populates="comments")

    replies = db.relationship(
        "Comment",
        backref=db.backref("parent", remote_side=[id]),
        lazy="dynamic",
        cascade="all, delete-orphan"
    )