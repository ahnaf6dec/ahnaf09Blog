from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, logout_user
from ..models.user import User
from ..extensions import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("Email already exists")
            return redirect("/register")

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Account created")
        return redirect("/login")

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid credentials")
            return redirect("/login")

        if user.is_banned:
            flash("Account banned")
            return redirect("/login")

        login_user(user)

        if user.is_admin:
            return redirect("/admin")

        return redirect("/")

    return render_template("login.html")






@auth_bp.route("/logout")
def logout():

    logout_user()

    return redirect("/")

