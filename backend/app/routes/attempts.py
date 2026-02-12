from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.attempt import Attempt
from app.models.attempt_score import AttemptScore
from app.models.flag import Flag
from app.services.scoring import score_attempt
from datetime import datetime

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

    attempt = Attempt.query.get_or_404(attempt_id)

    # Delete existing score
    AttemptScore.query.filter_by(
        attempt_id=attempt.id
    ).delete()

    db.session.flush()

    # Re-score
    score_attempt(attempt)

    # Only change to SCORED if not flagged
    if attempt.status != "FLAGGED":
        attempt.status = "SCORED"

    db.session.commit()

    return jsonify({
        "message": "Attempt recomputed",
        "attempt_id": str(attempt.id)
    }), 200
