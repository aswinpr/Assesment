from app.models.attempt import Attempt
from app.services.similarity import answer_similarity
from flask import current_app, g
from datetime import timedelta
import time

SIMILARITY_DUP_THRESHOLD = 0.99
SIMILARITY_FLAG_THRESHOLD = 0.90
TIME_WINDOW_MINUTES = 7


def deduplicate_attempt(new_attempt):

    start_time = time.time()

   
    # 7 Minute Window Calculation
   
    time_window_start = new_attempt.started_at - timedelta(minutes=TIME_WINDOW_MINUTES)
    time_window_end = new_attempt.started_at + timedelta(minutes=TIME_WINDOW_MINUTES)

   
    # Candidate Selection
   
    candidates = Attempt.query.filter(
        Attempt.test_id == new_attempt.test_id,
        Attempt.started_at >= time_window_start,
        Attempt.started_at <= time_window_end,
        Attempt.id != new_attempt.id
    ).all()

    best_similarity = 0
    best_match = None

    for attempt in candidates:
        similarity = answer_similarity(
            new_attempt.answers,
            attempt.answers
        )

        if similarity > best_similarity:
            best_similarity = similarity
            best_match = attempt

    decision = "INGESTED"
    canonical_id = None

   
    # Decision Logic
   

    if best_match is None:
        decision = "INGESTED"

    # Same student + high similarity + within 7 min → DEDUP
    elif (
        best_similarity >= SIMILARITY_DUP_THRESHOLD
        and new_attempt.student_id == best_match.student_id
    ):
        new_attempt.status = "DEDUPED"
        new_attempt.duplicate_of_attempt_id = best_match.id
        decision = "DEDUPED"
        canonical_id = best_match.id

    # Different student + high similarity → FLAG
    elif (
        best_similarity >= SIMILARITY_FLAG_THRESHOLD
        and new_attempt.student_id != best_match.student_id
    ):
        new_attempt.status = "FLAGGED"
        decision = "FLAGGED"
        canonical_id = best_match.id

    duration = round((time.time() - start_time) * 1000, 2)

   
    # Structured Dedup Log
   
    current_app.logger.info(
        "Dedup decision evaluated",
        extra={
            "channel": "dedup",
            "context": {
                "request_id": getattr(g, "request_id", None),
                "attempt_id": str(new_attempt.id),
                "student_id": str(new_attempt.student_id)
            },
            "extra_data": {
                "decision": decision,
                "similarity": round(best_similarity, 5),
                "canonical_id": str(canonical_id) if canonical_id else None,
                "candidates_checked": len(candidates),
                "time_window_minutes": TIME_WINDOW_MINUTES,
                "duration_ms": duration
            }
        }
    )

    return decision, best_similarity, canonical_id
