from ..extensions import db
from datetime import datetime

class Alert(db.Model):

    __tablename__ = "alert"

    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.Text, nullable=False)

    alert_type = db.Column(
        db.String(20),
        default="info"
    )  # success, danger, warning, info, primary

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )