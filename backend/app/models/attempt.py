import uuid
from app.extensions import db
from sqlalchemy.dialects.postgresql import JSONB


class Attempt(db.Model):
    __tablename__ = "attempts"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    student_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("students.id"))
    test_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tests.id"))

    student = db.relationship("Student", backref="attempts")
    test = db.relationship("Test", backref="attempts")  # ✅ REQUIRED

    source_event_id = db.Column(db.String, nullable=False)
    started_at = db.Column(db.DateTime(timezone=True), nullable=False)
    submitted_at = db.Column(db.DateTime(timezone=True))

    answers = db.Column(JSONB, nullable=False)
    raw_payload = db.Column(JSONB, nullable=False)

    status = db.Column(db.String, default="INGESTED")

    duplicate_of_attempt_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("attempts.id"),
        nullable=True
    )

    score = db.relationship(
        "AttemptScore",
        backref="attempt",
        uselist=False,
        cascade="all, delete-orphan"
    )

