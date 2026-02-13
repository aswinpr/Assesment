import uuid
from datetime import datetime
from app.extensions import db

class AttemptScore(db.Model):
    __tablename__ = "attempt_scores"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    attempt_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("attempts.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    total_questions = db.Column(db.Integer, nullable=False)
    correct = db.Column(db.Integer, nullable=False)
    incorrect = db.Column(db.Integer, nullable=False)
    skipped = db.Column(db.Integer, nullable=False)

    net_correct = db.Column(db.Integer)
    accuracy = db.Column(db.Float)

    raw_score = db.Column(db.Float, nullable=False)
    negative_score = db.Column(db.Float, nullable=False)
    final_score = db.Column(db.Float, nullable=False)

    explanation = db.Column(db.JSON, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
