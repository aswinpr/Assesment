from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.attempt import Attempt
from app.models.attempt_score import AttemptScore
from app.models.flag import Flag
from app.services.scoring import score_attempt
from datetime import datetime
from app.models.student import Student
from app.models.test import Test
from sqlalchemy import desc, asc
from app.services.datetime_utils import parse_iso_datetime


bp = Blueprint("attempts", __name__, url_prefix="/api/attempts")

@bp.route("/<uuid:attempt_id>/flag", methods=["POST"])
def manual_flag(attempt_id):

    attempt = Attempt.query.get_or_404(attempt_id)

    data = request.get_json() or {}
    reason = data.get("reason", "Manual review")

    # prevent duplicate flag rows
    existing_flag = Flag.query.filter_by(
        attempt_id=attempt.id,
        reason=reason
    ).first()

    if existing_flag:
        return jsonify({"message": "Already flagged"}), 200

    flag = Flag(
        attempt_id=attempt.id,
        reason=reason,
        created_at=datetime.utcnow(),
        details=data.get("details")
    )

    db.session.add(flag)

    attempt.status = "FLAGGED"

    db.session.commit()

    return jsonify({
        "message": "Attempt flagged",
        "attempt_id": str(attempt.id),
        "reason": reason
    }), 200


@bp.route("/<uuid:attempt_id>/recompute", methods=["POST"])
def recompute_attempt(attempt_id):

    attempt = Attempt.query.get(attempt_id)

    if not attempt:
        return jsonify({"error": "Attempt not found"}), 404

    # Do not recompute DEDUPED attempts
    if attempt.status == "DEDUPED":
        return jsonify({"error": "Cannot recompute deduplicated attempt"}), 400

    # Remove existing score
    existing_score = AttemptScore.query.filter_by(
        attempt_id=attempt.id
    ).first()

    if existing_score:
        db.session.delete(existing_score)
        db.session.flush()

    # Recompute score
    new_score = score_attempt(attempt)

    # If not manually flagged → set to SCORED
    has_manual_flag = Flag.query.filter_by(
        attempt_id=attempt.id
    ).first()

    if not has_manual_flag:
        attempt.status = "SCORED"

    db.session.commit()

    return jsonify({
        "attempt_id": str(attempt.id),
        "new_score": new_score.final_score,
        "status": attempt.status,
        "message": "Recomputed successfully"
    }), 200



@bp.route("", methods=["GET"])
def list_attempts():

   
    # Query Parameters
   
    test_id = request.args.get("test_id")
    student_id = request.args.get("student_id")
    status = request.args.get("status")
    has_duplicates = request.args.get("has_duplicates")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 20))

   
    # Base Query
   
    query = (
        db.session.query(Attempt)
        .outerjoin(AttemptScore, AttemptScore.attempt_id == Attempt.id)
        .outerjoin(Student, Student.id == Attempt.student_id)
        .outerjoin(Test, Test.id == Attempt.test_id)
    )

   
    # Filters
   

    if test_id:
        query = query.filter(Attempt.test_id == test_id)

    if student_id:
        query = query.filter(Attempt.student_id == student_id)

    if status:
        query = query.filter(Attempt.status == status)

    if has_duplicates:
        if has_duplicates.lower() == "true":
            query = query.filter(Attempt.duplicate_of_attempt_id.isnot(None))
        elif has_duplicates.lower() == "false":
            query = query.filter(Attempt.duplicate_of_attempt_id.is_(None))

    if date_from:
        parsed_from = parse_iso_datetime(date_from)
        if parsed_from:
            query = query.filter(Attempt.submitted_at >= parsed_from)

    if date_to:
        parsed_to = parse_iso_datetime(date_to)
        if parsed_to:
            query = query.filter(Attempt.submitted_at <= parsed_to)

   
    # Default Sorting
   
    query = query.order_by(desc(Attempt.submitted_at))

    total = query.count()

    attempts = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

   
    # Response
   
    response = []

    for attempt in attempts:
        score = None
        if attempt.score:
            score = attempt.score.final_score

        response.append({
            "attempt_id": str(attempt.id),
            "student_id": str(attempt.student_id),
            "student_name": attempt.student.full_name,
            "test_id": str(attempt.test_id),
            "test_name": attempt.test.name,
            "status": attempt.status,
            "final_score": score,
            "submitted_at": attempt.submitted_at
        })

    return jsonify({
        "total": total,
        "page": page,
        "limit": limit,
        "data": response
    }), 200