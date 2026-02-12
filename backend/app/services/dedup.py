from datetime import timedelta
from app.models.attempt import Attempt
from app.extensions import db
from app.services.similarity import answer_similarity

SIMILARITY_THRESHOLD = 0.92
TIME_WINDOW_MINUTES = 7


def deduplicate_attempt(new_attempt: Attempt):
    """
    Checks if new_attempt is a duplicate of an existing attempt.
    Ensures:
    - Only one canonical attempt
    - All duplicates point to canonical.id
    """

    window_start = new_attempt.started_at - timedelta(minutes=TIME_WINDOW_MINUTES)
    window_end = new_attempt.started_at + timedelta(minutes=TIME_WINDOW_MINUTES)

    candidates = Attempt.query.filter(
        Attempt.student_id == new_attempt.student_id,
        Attempt.test_id == new_attempt.test_id,
        Attempt.started_at.between(window_start, window_end),
        Attempt.id != new_attempt.id,
        Attempt.status != "DEDUPED"  
    ).all()

    for candidate in candidates:
        similarity = answer_similarity(
            new_attempt.answers, candidate.answers
        )

        if similarity >= SIMILARITY_THRESHOLD:
            # pick canonical (earliest started_at)
            if candidate.started_at <= new_attempt.started_at:
                canonical = candidate
                duplicate = new_attempt
            else:
                canonical = new_attempt
                duplicate = candidate

            duplicate.status = "DEDUPED"
            duplicate.duplicate_of_attempt_id = canonical.id

            db.session.flush()
            return True, similarity, canonical.id

    return False, None, None

