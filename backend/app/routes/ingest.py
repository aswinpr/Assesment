from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.student import Student
from app.models.test import Test
from app.models.attempt import Attempt
from app.services.identity import normalize_email, normalize_phone
from app.services.datetime_utils import parse_iso_datetime
from app.services.dedup import deduplicate_attempt

bp = Blueprint("ingest", __name__, url_prefix="/api/ingest")


@bp.route("/attempts", methods=["POST"])
def ingest_attempts():
    events = request.get_json()
    if not isinstance(events, list):
        return jsonify({"error": "Expected list of attempts"}), 400

    ingested = 0
    deduped = 0
    skipped_invalid_timestamp = 0

    for event in events:
        # Safe datetime parsing
        started_at = parse_iso_datetime(event.get("started_at"))
        submitted_at = parse_iso_datetime(event.get("submitted_at"))

        if not started_at:
            skipped_invalid_timestamp += 1
            continue

        student_data = event["student"]
        test_data = event["test"]

        email = student_data.get("email")
        phone = student_data.get("phone")

        # Student resolution
        if email:
            email = normalize_email(email)
            student = Student.query.filter_by(email=email).first()
        else:
            phone = normalize_phone(phone)
            student = Student.query.filter_by(phone=phone).first()

        if not student:
            student = Student(
                full_name=student_data["full_name"],
                email=email,
                phone=phone
            )
            db.session.add(student)
            db.session.flush()

        # Test resolution
        test = Test.query.filter_by(name=test_data["name"]).first()
        if not test:
            test = Test(
                name=test_data["name"],
                max_marks=test_data["max_marks"],
                negative_marking=test_data["negative_marking"]
            )
            db.session.add(test)
            db.session.flush()

        # Create attempt
        attempt = Attempt(
            student_id=student.id,
            test_id=test.id,
            source_event_id=event["source_event_id"],
            started_at=started_at,
            submitted_at=submitted_at,
            answers=event["answers"],
            raw_payload=event,
            status="INGESTED"
        )

        db.session.add(attempt)
        db.session.flush()

        # Deduplication
        is_dup, similarity, canonical_id = deduplicate_attempt(attempt)
        if is_dup:
            deduped += 1

        ingested += 1

    db.session.commit()

    return jsonify({
        "ingested": ingested,
        "deduped": deduped,
        "skipped_invalid_timestamp": skipped_invalid_timestamp
    }), 201
