import uuid
from datetime import datetime
from app.extensions import db

class Test(db.Model):
    __tablename__ = "tests"

    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = db.Column(db.String, nullable=False)

    max_marks = db.Column(db.Integer, nullable=False)

    # ✅ store as numeric value, NOT JSON
    negative_marking = db.Column(db.Float, nullable=False, default=0.0)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow
    )
