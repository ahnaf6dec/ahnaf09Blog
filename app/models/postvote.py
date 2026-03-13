from ..extensions import db
from datetime import datetime

class PostVote(db.Model):
    __tablename__ = "post_vote"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    vote_type = db.Column(db.String(10), nullable=False)  # "upvote" or "downvote"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Prevent the same user from voting multiple times on the same post
    __table_args__ = (
        db.UniqueConstraint("user_id", "post_id", name="unique_user_post_vote"),
    )

    # Relationships
    user = db.relationship("User", backref=db.backref("post_votes", lazy="dynamic"))
    post = db.relationship("Post", backref=db.backref("post_votes", lazy="dynamic"))
