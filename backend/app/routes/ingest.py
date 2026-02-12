from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.student import Student
from app.models.test import Test
from app.models.attempt import Attempt
from app.services.identity import normalize_email, normalize_phone
from app.services.datetime_utils import parse_iso_datetime
from app.services.dedup import deduplicate_attempt
from app.services.scoring import score_attempt
from app.models.attempt_score import AttemptScore

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
        try:
            # ---- Safe datetime parsing ----
            started_at = parse_iso_datetime(event.get("started_at"))
            submitted_at = parse_iso_datetime(event.get("submitted_at"))

            if not started_at:
                skipped_invalid_timestamp += 1
                continue

            student_data = event["student"]
            test_data = event["test"]

            # ---- Student resolution ----
            email = student_data.get("email")
            phone = student_data.get("phone")

            student = None
            if email:
                email = normalize_email(email)
                student = Student.query.filter_by(email=email).first()
            elif phone:
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

            # ---- Test resolution ----
            test = Test.query.filter_by(name=test_data["name"]).first()

            if not test:

                negative_marking = test_data.get("negative_marking", 0)

                # If JSON object → extract per_question
                if isinstance(negative_marking, dict):
                    negative_marking = negative_marking.get("per_question", 0)

                test = Test(
                    name=test_data["name"],
                    max_marks=test_data["max_marks"],
                    negative_marking=float(negative_marking)
                )

                db.session.add(test)
                db.session.flush()


            # ---- Create Attempt ----
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

            # ---- Deduplication ----
            is_dup, similarity, canonical_id = deduplicate_attempt(attempt)

            if is_dup:
                deduped += 1
                continue  # do NOT score duplicates

            ## ---- Canonical attempt ----
            ingested += 1

            score_attempt(attempt)
            attempt.status = "SCORED"


        except Exception as e:
            print("ERROR DURING INGEST:", str(e))
            db.session.rollback()
            continue


    db.session.commit()

    return jsonify({
        "ingested": ingested,
        "deduped": deduped,
        "skipped_invalid_timestamp": skipped_invalid_timestamp
    }), 201
