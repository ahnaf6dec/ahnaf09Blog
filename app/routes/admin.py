from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from ..extensions import db
from ..models.user import User
from ..models.post import Post
from ..models.comment import Comment
from ..models.category import Category
from ..models.tag import Tag
from ..models.contact import Contact
from ..models.postvote import PostVote
from ..models.alert import Alert
from ..models.about import About
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ==============================
# ADMIN PERMISSION DECORATOR
# ==============================
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        if not current_user.is_admin:
            return "Access Denied", 403
        return func(*args, **kwargs)
    return wrapper

# ==============================
# DASHBOARD
# ==============================
@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    total_posts = Post.query.count()
    total_comments = Comment.query.count()
    total_contacts = Contact.query.count()

    top_upvoted = (
        db.session.query(Post, func.count(PostVote.id).label("votes"))
        .join(PostVote)
        .filter(PostVote.vote_type == "upvote")
        .group_by(Post.id)
        .order_by(func.count(PostVote.id).desc())
        .first()
    )

    worst_post = (
        db.session.query(Post, func.count(PostVote.id).label("votes"))
        .join(PostVote)
        .filter(PostVote.vote_type == "downvote")
        .group_by(Post.id)
        .order_by(func.count(PostVote.id).desc())
        .first()
    )

    return render_template("admin/dashboard.html",
                           total_users=total_users,
                           total_posts=total_posts,
                           total_comments=total_comments,
                           total_contacts=total_contacts,
                           top_upvoted=top_upvoted[0] if top_upvoted else None,
                           top_upvotes=top_upvoted[1] if top_upvoted else 0,
                           worst_post=worst_post[0] if worst_post else None,
                           worst_downvotes=worst_post[1] if worst_post else 0)

# ==============================
# POSTS MANAGEMENT
# ==============================
@admin_bp.route("/posts")
@login_required
@admin_required
def posts():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")
    category_id = request.args.get("category", type=int)
    tag_id = request.args.get("tag", type=int)

    query = Post.query
    if search:
        query = query.filter(Post.title.ilike(f"%{search}%") | Post.slug.ilike(f"%{search}%"))
    if category_id:
        query = query.filter(Post.category_id == category_id)
    if tag_id:
        query = query.filter(Post.tags.any(id=tag_id))

    posts_paginated = query.order_by(Post.created_at.desc()).paginate(page=page, per_page=5, error_out=False)
    categories = Category.query.all()
    tags = Tag.query.all()

    return render_template("admin/posts.html",
                           posts=posts_paginated,
                           categories=categories,
                           tags=tags,
                           search=search,
                           category_id=category_id,
                           tag_id=tag_id)

@admin_bp.route("/post/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_post():
    categories = Category.query.all()
    tags = Tag.query.all()
    if request.method == "POST":
        title = request.form.get("title")
        slug = request.form.get("slug")
        content = request.form.get("content")
        category_id = request.form.get("category", type=int)
        tag_id = request.form.get("tag", type=int)

        if Post.query.filter_by(slug=slug).first():
            flash("Slug already exists!", "danger")
            return redirect(url_for("admin.add_post"))

        post = Post(title=title, slug=slug, content=content, category_id=category_id, author_id=current_user.id)
        if tag_id:
            tag = Tag.query.get(tag_id)
            if tag:
                post.tags = [tag]

        db.session.add(post)
        db.session.commit()
        flash("Post added successfully!", "success")
        return redirect(url_for("admin.posts"))

    return render_template("admin/add_post.html", categories=categories, tags=tags)

@admin_bp.route("/post/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    categories = Category.query.all()
    tags = Tag.query.all()
    tag_id = post.tags[0].id if post.tags else None

    if request.method == "POST":
        title = request.form.get("title")
        slug = request.form.get("slug")
        content = request.form.get("content")
        category_id = request.form.get("category", type=int)
        tag_id = request.form.get("tag", type=int)

        if post.slug != slug and Post.query.filter_by(slug=slug).first():
            flash("Slug already exists!", "danger")
            return redirect(url_for("admin.edit_post", post_id=post_id))

        post.title = title
        post.slug = slug
        post.content = content
        post.category_id = category_id
        post.tags = [Tag.query.get(tag_id)] if tag_id else []

        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for("admin.posts"))

    return render_template("admin/edit_post.html", post=post, categories=categories, tags=tags, tag_id=tag_id)

@admin_bp.route("/post/delete/<int:post_id>", methods=["POST"])
@login_required
@admin_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!", "success")
    return redirect(url_for("admin.posts"))

# Category

@admin_bp.route("/categories")
@login_required
@admin_required
def categories():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")
    filter_id = request.args.get("filter", type=int)  # New filter param

    query = Category.query

    # Search by category name or slug
    if search:
        query = query.filter(
            Category.name.ilike(f"%{search}%") |
            Category.slug.ilike(f"%{search}%")
        )

    # Filter by category id if provided
    if filter_id:
        query = query.filter(Category.id == filter_id)

    # Pagination
    categories_paginated = query.order_by(Category.id.desc()).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    # All categories for filter dropdown
    all_categories = Category.query.order_by(Category.name).all()

    return render_template(
        "admin/categories.html",
        categories=categories_paginated,
        all_categories=all_categories,
        search=search,
        filter_id=filter_id
    )


# ADD CATEGORY
@admin_bp.route("/category/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_category():
    if request.method == "POST":
        name = request.form.get("name")
        slug = request.form.get("slug")

        if Category.query.filter_by(slug=slug).first():
            flash("Slug already exists!", "danger")
            return redirect(url_for("admin.add_category"))

        category = Category(name=name, slug=slug)
        db.session.add(category)
        db.session.commit()

        flash("Category added successfully!", "success")
        return redirect(url_for("admin.categories"))

    return render_template("admin/add_category.html")


# EDIT CATEGORY
@admin_bp.route("/category/edit/<int:category_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)

    if request.method == "POST":
        name = request.form.get("name")
        slug = request.form.get("slug")

        # check slug uniqueness
        existing = Category.query.filter_by(slug=slug).first()
        if existing and existing.id != category.id:
            flash("Slug already exists!", "danger")
            return redirect(url_for("admin.edit_category", category_id=category.id))

        category.name = name
        category.slug = slug
        db.session.commit()

        flash("Category updated successfully!", "success")
        return redirect(url_for("admin.categories"))

    return render_template("admin/edit_category.html", category=category)


# DELETE CATEGORY
@admin_bp.route("/category/delete/<int:category_id>", methods=["POST"])
@login_required
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)

    db.session.delete(category)
    db.session.commit()

    flash("Category deleted successfully!", "success")
    return redirect(url_for("admin.categories"))



# ==============================
# TAG MANAGEMENT
# ==============================

@admin_bp.route("/tags")
@login_required
@admin_required
def tags():
    page = request.args.get("page", 1, type=int)
    search_tag = request.args.get("search_tag", "")
    search_post = request.args.get("search_post", "")
    filter_tag_id = request.args.get("filter", type=int)

    query = Tag.query

    # Search by tag name
    if search_tag:
        query = query.filter(Tag.name.ilike(f"%{search_tag}%"))

    # Filter by tag id (if a specific tag is selected)
    if filter_tag_id:
        query = query.filter(Tag.id == filter_tag_id)

    # Join with posts for search_post
    if search_post:
        query = query.join(Tag.posts).filter(
            db.or_(
                Post.title.ilike(f"%{search_post}%"),
                Post.slug.ilike(f"%{search_post}%")
            )
        ).distinct()

    # Pagination
    tags_paginated = query.order_by(Tag.id.desc()).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    all_tags = Tag.query.order_by(Tag.name).all()

    return render_template(
        "admin/tags.html",
        tags=tags_paginated,
        all_tags=all_tags,
        search_tag=search_tag,
        search_post=search_post,
        filter_tag_id=filter_tag_id
    )


# ADD TAG
@admin_bp.route("/tag/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_tag():
    if request.method == "POST":
        name = request.form.get("name")

        if Tag.query.filter_by(name=name).first():
            flash("Tag already exists!", "danger")
            return redirect(url_for("admin.add_tag"))

        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()

        flash("Tag added successfully!", "success")
        return redirect(url_for("admin.tags"))

    return render_template("admin/add_tag.html")


# EDIT TAG
@admin_bp.route("/tag/edit/<int:tag_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    if request.method == "POST":
        name = request.form.get("name")

        existing = Tag.query.filter_by(name=name).first()
        if existing and existing.id != tag.id:
            flash("Tag name already exists!", "danger")
            return redirect(url_for("admin.edit_tag", tag_id=tag.id))

        tag.name = name
        db.session.commit()

        flash("Tag updated successfully!", "success")
        return redirect(url_for("admin.tags"))

    return render_template("admin/edit_tag.html", tag=tag)


# DELETE TAG
@admin_bp.route("/tag/delete/<int:tag_id>", methods=["POST"])
@login_required
@admin_required
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    flash("Tag deleted successfully!", "success")
    return redirect(url_for("admin.tags"))

# ==============================
# USERS MANAGEMENT
# ==============================
@admin_bp.route("/users")
@login_required
@admin_required
def users():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")
    status = request.args.get("status", "all")

    query = User.query
    if search:
        query = query.filter(User.username.ilike(f"%{search}%") | User.email.ilike(f"%{search}%"))

    if status == "banned":
        query = query.filter_by(is_banned=True)
    elif status == "active":
        query = query.filter_by(is_banned=False)

    users_paginated = query.order_by(User.id.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template("admin/users.html", users=users_paginated, search=search, status=status)

@admin_bp.route("/ban/<int:user_id>")
@login_required
@admin_required
def ban_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_banned = True
    db.session.commit()
    flash(f"{user.username} has been banned.", "success")
    return redirect(url_for("admin.users"))

@admin_bp.route("/unban/<int:user_id>")
@login_required
@admin_required
def unban_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_banned = False
    db.session.commit()
    flash(f"{user.username} has been unbanned.", "success")
    return redirect(url_for("admin.users"))

@admin_bp.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot delete your own account!", "danger")
        return redirect(url_for("admin.users"))
    db.session.delete(user)
    db.session.commit()
    flash(f"{user.username} has been deleted.", "success")
    return redirect(url_for("admin.users"))

# ==============================
# COMMENTS MANAGEMENT
# ==============================
@admin_bp.route("/comments")
@login_required
@admin_required
def comments():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")

    query = Comment.query.options(joinedload(Comment.user), joinedload(Comment.post))
    if search:
        search_pattern = f"%{search}%"
        query = query.join(User).filter(
            db.or_(
                User.username.ilike(search_pattern),
                Comment.content.ilike(search_pattern)
            )
        )

    comments_paginated = query.order_by(Comment.created_at.desc()).paginate(page=page, per_page=5, error_out=False)
    return render_template("admin/comments.html", comments=comments_paginated, search=search)

@admin_bp.route("/comment/delete/<int:comment_id>", methods=["POST"])
@login_required
@admin_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted successfully.", "success")
    return redirect(url_for("admin.comments"))

# ==============================
# CONTACT MANAGEMENT
# ==============================
@admin_bp.route("/contacts")
@login_required
@admin_required
def contacts():
    page = request.args.get("page", 1, type=int)
    search_email = request.args.get("search_email", "")
    query = Contact.query
    if search_email:
        query = query.filter(Contact.email.ilike(f"%{search_email}%"))
    contacts_paginated = query.order_by(Contact.id.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template("admin/contacts.html", contacts=contacts_paginated, search_email=search_email)

@admin_bp.route("/contact/delete/<int:contact_id>", methods=["POST"])
@login_required
@admin_required
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    flash("Contact deleted successfully!", "success")
    return redirect(url_for("admin.contacts"))

# ==============================
# ALERT MANAGEMENT
# ==============================
@admin_bp.route("/alerts")
@login_required
@admin_required
def alerts():
    alerts = Alert.query.order_by(Alert.created_at.desc()).all()
    return render_template("admin/alerts.html", alerts=alerts)

@admin_bp.route("/alerts/create", methods=["POST"])
@login_required
@admin_required
def create_alert():
    message = request.form.get("message")
    alert_type = request.form.get("alert_type", "info")
    alert = Alert(message=message, alert_type=alert_type)
    db.session.add(alert)
    db.session.commit()
    flash("Alert created successfully!", "success")
    return redirect(url_for("admin.alerts"))


# Delete Alert
@admin_bp.route("/alerts/delete/<int:id>", methods=["POST"])
@login_required
@admin_required
def delete_alert(id):
    alert = Alert.query.get_or_404(id)
    db.session.delete(alert)
    db.session.commit()
    flash("Alert deleted!", "success")
    return redirect(url_for("admin.alerts"))

# Edit Alert
@admin_bp.route("/alerts/edit/<int:alert_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_alert(alert_id):
    alert = Alert.query.get_or_404(alert_id)
    if request.method == "POST":
        alert.message = request.form.get("message")
        alert.alert_type = request.form.get("alert_type", "info")
        db.session.commit()
        flash("Alert updated!", "success")
        return redirect(url_for("admin.alerts"))
    return render_template("admin/edit_alert.html", alert=alert)



@admin_bp.route("/about", methods=["GET", "POST"])
@login_required
@admin_required
def about():
    about_entry = About.query.first()
    if request.method == "POST":
        avatar_url = request.form.get("avatar_url")
        name = request.form.get("name")
        bio = request.form.get("bio")
        social_link = request.form.get("social_link")
        
        if about_entry:
            # Update existing
            about_entry.avatar_url = avatar_url
            about_entry.name = name
            about_entry.bio = bio
            about_entry.social_link = social_link
        else:
            # Create new
            about_entry = About(
                avatar_url=avatar_url,
                name=name,
                bio=bio,
                social_link=social_link
            )
            db.session.add(about_entry)
        
        db.session.commit()
        flash("About section updated successfully!", "success")
        return redirect(url_for("admin.about"))
    
    return render_template("admin/about.html", about=about_entry)