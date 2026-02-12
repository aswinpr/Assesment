import uuid
from datetime import datetime
from app.extensions import db
from sqlalchemy.dialects.postgresql import JSONB

class Test(db.Model):
    __tablename__ = "tests"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    max_marks = db.Column(db.Integer, nullable=False)

    negative_marking = db.Column(db.Float, nullable=False)   # ← FIXED

    answer_key = db.Column(JSONB, nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow
    )
