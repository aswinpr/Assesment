from app.models.student import Student
from flask import Blueprint, jsonify
from sqlalchemy import func
from app.extensions import db
from app.models.test import Test
from app.models.attempt import Attempt
from app.models.attempt_score import AttemptScore  
from sqlalchemy import desc, asc
from flask import request

bp = Blueprint("analytics", __name__, url_prefix="/api/analytics")


@bp.route("/test-summary", methods=["GET"])
def test_summary():

    results = (
        db.session.query(
            Test.id.label("test_id"),
            Test.name.label("test_name"),
            func.count(Attempt.id).label("total_attempts"),
            func.count(
                func.nullif(Attempt.status != "SCORED", True)
            ).label("scored_attempts"),
            func.avg(AttemptScore.final_score).label("avg_score"),
            func.max(AttemptScore.final_score).label("highest_score"),
            func.min(AttemptScore.final_score).label("lowest_score"),
            func.count(
                func.nullif(Attempt.status != "DEDUPED", True)
            ).label("dedup_count"),
            func.count(
                func.nullif(Attempt.status != "FLAGGED", True)
            ).label("flagged_count"),
        )
        .outerjoin(Attempt, Attempt.test_id == Test.id)
        .outerjoin(AttemptScore, AttemptScore.attempt_id == Attempt.id)
        .group_by(Test.id)
        .all()
    )

    response = []

    for row in results:
        response.append({
            "test_id": str(row.test_id),
            "test_name": row.test_name,
            "total_attempts": row.total_attempts or 0,
            "scored_attempts": row.scored_attempts or 0,
            "average_score": float(row.avg_score or 0),
            "highest_score": float(row.highest_score or 0),
            "lowest_score": float(row.lowest_score or 0),
            "dedup_count": row.dedup_count or 0,
            "flagged_count": row.flagged_count or 0,
        })

    return jsonify(response), 200


@bp.route("/leaderboard", methods=["GET"])
def leaderboard():

    test_id = request.args.get("test_id")
    if not test_id:
        return jsonify({"error": "test_id is required"}), 400

    attempts = (
        db.session.query(Attempt)
        .join(AttemptScore, AttemptScore.attempt_id == Attempt.id)
        .join(Student, Student.id == Attempt.student_id)
        .filter(
            Attempt.test_id == test_id,
            Attempt.status == "SCORED"
        )
        .order_by(AttemptScore.final_score.desc())
        .all()
    )

    leaderboard_data = []
    prev_score = None
    dense_rank = 0

    for attempt in attempts:

        score_obj = attempt.score  # use stored score

        score = score_obj.final_score

        if score != prev_score:
            dense_rank += 1
        prev_score = score

        leaderboard_data.append({
            "attempt_id": str(attempt.id),
            "rank": dense_rank,
            "student_name": attempt.student.full_name,
            "score": score_obj.final_score,
            "correct": score_obj.correct,
            "incorrect": score_obj.incorrect,
            "skipped": score_obj.skipped,
            "accuracy": score_obj.accuracy
        })

    return jsonify(leaderboard_data), 200

