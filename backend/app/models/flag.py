import uuid
from datetime import datetime
from app.extensions import db
from sqlalchemy.dialects.postgresql import JSONB


class Flag(db.Model):
    __tablename__ = "flags"

    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    attempt_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("attempts.id"),
        nullable=False
    )

    reason = db.Column(db.String, nullable=False)

    details = db.Column(db.JSON)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow
    )
