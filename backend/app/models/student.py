import uuid
from datetime import datetime
from app.extensions import db

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True, index=True)
    phone = db.Column(db.String, nullable=True, index=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow
    )
