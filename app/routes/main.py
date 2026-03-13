# app/routes/main.py
from flask import Blueprint, render_template, request
from ..models.post import Post
from ..models.category import Category
from ..models.tag import Tag
from ..models.alert import Alert
from ..models.about import About

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def index():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")
    tag_id = request.args.get("tag", type=int)
    category_id = request.args.get("category", type=int)

    # Base query
    query = Post.query

    # Apply search filter
    if search:
        query = query.filter(
            Post.title.ilike(f"%{search}%") |
            Post.slug.ilike(f"%{search}%")
        )

    # Filter by tag
    if tag_id:
        query = query.filter(Post.tags.any(id=tag_id))

    # Filter by category
    if category_id:
        query = query.filter(Post.category_id == category_id)

    # Pagination
    posts_paginated = query.order_by(Post.created_at.desc()).paginate(
        page=page,
        per_page=5,
        error_out=False
    )

    # Sidebar & alerts
    categories = Category.query.order_by(Category.name).all()
    tags = Tag.query.order_by(Tag.name).all()
    alerts = Alert.query.filter_by(is_active=True).order_by(Alert.created_at.desc()).all()

    # About section
    about_entry = About.query.first()

    return render_template(
        "index.html",
        posts=posts_paginated,
        categories=categories,
        tags=tags,
        alerts=alerts,
        search=search,
        tag_id=tag_id,
        category_id=category_id,
        about=about_entry
    )

# -------------------------------
# Terms & Conditions route
# -------------------------------
@main_bp.route("/terms", methods=["GET"])
def terms():
    return render_template("terms.html")