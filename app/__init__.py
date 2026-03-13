from flask import Flask
from .config import Config
from .extensions import db, login_manager, bcrypt, migrate

# Factory function
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Import all models so Flask-Migrate can detect them
    with app.app_context():
        from .models.user import User
        from .models.post import Post
        from .models.comment import Comment
        from .models.category import Category
        from .models.tag import Tag
        from .models.like import Like
        from .models.bookmark import Bookmark
        from .models.contact import Contact
        from .models.postvote import PostVote
        from .models.alert import Alert
        from .models.about import About

        # Create tables if not exist (optional)
        # db.create_all()

    # Import and register blueprints
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.profile import profile_bp
    from .routes.blog import blog_bp
    from .routes.contact import contact_bp
    from .routes.upload import upload_bp
    from .routes.admin import admin_bp
    from .routes.comments import comments_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(comments_bp)

    return app


# Expose app for Flask CLI
app = create_app()


# Flask-Login user loader
from .models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))