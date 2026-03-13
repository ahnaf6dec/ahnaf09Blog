from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from ..extensions import db

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET","POST"])
@login_required
def profile():

    if request.method == "POST":

        new_password = request.form["password"]

        current_user.set_password(new_password)

        db.session.commit()

        return redirect("/profile")

    return render_template("profile.html")