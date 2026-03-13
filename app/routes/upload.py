import os
from flask import Blueprint, request, current_app, jsonify
from werkzeug.utils import secure_filename

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload-image", methods=["POST"])
def upload_image():

    file = request.files["image"]

    filename = secure_filename(file.filename)

    path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )

    os.makedirs(os.path.dirname(path), exist_ok=True)

    file.save(path)

    return jsonify({
        "url": "/static/uploads/" + filename
    })