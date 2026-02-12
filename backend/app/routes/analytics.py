from flask import Blueprint, jsonify
from sqlalchemy import func
from app.extensions import db
from app.models.test import Test
from app.models.attempt import Attempt
from app.models.attempt_score import AttemptScore  

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
