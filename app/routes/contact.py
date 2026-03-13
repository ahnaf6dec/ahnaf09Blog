from flask import Blueprint, render_template, request
from ..extensions import db
from ..models.contact import Contact

contact_bp = Blueprint("contact", __name__)

@contact_bp.route("/contact", methods=["GET","POST"])
def contact():

    if request.method == "POST":

        email = request.form["email"]
        message = request.form["message"]

        c = Contact(email=email, message=message)

        db.session.add(c)
        db.session.commit()

    return render_template("contact.html")