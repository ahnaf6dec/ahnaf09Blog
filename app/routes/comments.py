# routes/comments.py
from flask import Blueprint, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from ..extensions import db
from ..models.comment import Comment
from ..models.post import Post

comments_bp = Blueprint("comments", __name__)

# ---------------- CREATE COMMENT ----------------
@comments_bp.route("/comment/create/<int:post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get("content", "").strip()
    if not content:
        flash("Comment cannot be empty", "danger")
        return redirect(request.referrer)

    comment = Comment(
        content=content,
        user_id=current_user.id,
        post_id=post.id,
        parent_id=None  # top-level comment
    )
    db.session.add(comment)
    db.session.commit()
    flash("Comment posted", "success")
    return redirect(request.referrer)


# ---------------- REPLY COMMENT ----------------
@comments_bp.route("/comment/reply/<int:comment_id>", methods=["POST"])
@login_required
def reply_comment(comment_id):
    parent = Comment.query.get_or_404(comment_id)
    content = request.form.get("content", "").strip()
    if not content:
        flash("Reply cannot be empty", "danger")
        return redirect(request.referrer)

    reply = Comment(
        content=content,
        user_id=current_user.id,
        post_id=parent.post_id,
        parent_id=parent.id
    )
    db.session.add(reply)
    db.session.commit()
    flash("Reply posted", "success")
    return redirect(request.referrer)


# ---------------- EDIT COMMENT / REPLY ----------------
@comments_bp.route("/comment/edit/<int:id>", methods=["POST"])
@login_required
def edit_comment(id):
    comment = Comment.query.get_or_404(id)

    # only owner can edit & not deleted
    if comment.user_id != current_user.id or comment.is_deleted:
        abort(403)

    content = request.form.get("content", "").strip()
    if not content:
        flash("Content cannot be empty", "danger")
        return redirect(request.referrer)

    comment.content = content
    db.session.commit()
    flash("Comment updated!", "success")
    return redirect(request.referrer)


# ---------------- DELETE COMMENT / REPLY (Soft Delete) ----------------
@comments_bp.route("/comment/delete/<int:id>", methods=["POST"])
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)

    # only owner can delete
    if comment.user_id != current_user.id:
        abort(403)

    # soft delete
    if comment.parent_id is None:
        comment.content = "Comment deleted"
    else:
        comment.content = "Reply deleted"

    comment.is_deleted = True
    db.session.commit()
    flash("Deleted successfully", "success")
    return redirect(request.referrer)