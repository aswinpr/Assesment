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
    from flask import request

    test_id = request.args.get("test_id")

    if not test_id:
        return jsonify({"error": "test_id is required"}), 400

    results = (
        db.session.query(
            Attempt.id.label("attempt_id"),
            Attempt.submitted_at,
            AttemptScore.final_score,
            Student.full_name.label("student_name")
        )
        .join(AttemptScore, AttemptScore.attempt_id == Attempt.id)
        .join(Student, Student.id == Attempt.student_id)
        .filter(Attempt.test_id == test_id)
        .filter(Attempt.status == "SCORED")
        .order_by(
            AttemptScore.final_score.desc(),
            Attempt.submitted_at.asc()
        )
        .all()
    )

    leaderboard = []
    current_rank = 0
    last_score = None

    for index, row in enumerate(results):

        # Dense ranking logic
        if row.final_score != last_score:
            current_rank += 1
            last_score = row.final_score

        leaderboard.append({
            "attempt_id": str(row.attempt_id),
            "student_name": row.student_name,
            "score": float(row.final_score),
            "rank": current_rank,
            "submitted_at": row.submitted_at
        })

    return jsonify(leaderboard), 200
