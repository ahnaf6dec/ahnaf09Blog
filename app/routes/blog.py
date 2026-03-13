from flask import Blueprint, render_template, request, redirect, jsonify
from flask_login import current_user, login_required
from ..models.post import Post
from ..models.comment import Comment
from ..models.postvote import PostVote
from ..extensions import db
from datetime import datetime

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/post/<slug>", methods=["GET","POST"])
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    # Increment view count
    post.views += 1
    db.session.commit()
    
    if request.method == "POST":
        if not current_user.is_authenticated:
            return redirect("/login")

        content = request.form["content"]

        comment = Comment(
            content=content,
            user_id=current_user.id,
            post_id=post.id,
            created_at=datetime.utcnow()
        )

        db.session.add(comment)
        db.session.commit()
        return redirect(request.url)

    # fetch all comments
    comments = Comment.query.filter_by(post_id=post.id).all()

    # fetch vote counts
    upvotes_count = PostVote.query.filter_by(post_id=post.id, vote_type="upvote").count()
    downvotes_count = PostVote.query.filter_by(post_id=post.id, vote_type="downvote").count()

    return render_template(
        "post.html",
        post=post,
        comments=comments,
        upvotes_count=upvotes_count,
        downvotes_count=downvotes_count
    )


@blog_bp.route("/post/<int:post_id>/vote", methods=["POST"])
@login_required
def vote_post(post_id):
    post = Post.query.get_or_404(post_id)

    if not request.is_json:
        return jsonify({"error": "Invalid request"}), 400

    data = request.get_json()
    vote_type = data.get("vote_type")

    if vote_type not in ["upvote", "downvote"]:
        return jsonify({"error": "Invalid vote type"}), 400

    vote = PostVote.query.filter_by(user_id=current_user.id, post_id=post.id).first()

    if vote:
        if vote.vote_type == vote_type:
            # undo vote
            db.session.delete(vote)
        else:
            vote.vote_type = vote_type
    else:
        vote = PostVote(user_id=current_user.id, post_id=post.id, vote_type=vote_type)
        db.session.add(vote)

    db.session.commit()

    upvotes_count = PostVote.query.filter_by(post_id=post.id, vote_type="upvote").count()
    downvotes_count = PostVote.query.filter_by(post_id=post.id, vote_type="downvote").count()

    return jsonify({"upvotes": upvotes_count, "downvotes": downvotes_count, "your_vote": vote_type})