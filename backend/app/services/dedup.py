from app.models.attempt import Attempt
from app.services.similarity import answer_similarity

SIMILARITY_DUP_THRESHOLD = 0.99
SIMILARITY_FLAG_THRESHOLD = 0.90


def deduplicate_attempt(new_attempt):

    candidates = Attempt.query.filter(
        Attempt.test_id == new_attempt.test_id,
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

    if best_match is None:
        return "INGESTED", 0, None

    if best_similarity >= 0.99:
        new_attempt.status = "DEDUPED"
        new_attempt.duplicate_of_attempt_id = best_match.id
        return "DEDUPED", best_similarity, best_match.id

    if (
        best_similarity >= 0.90
        and new_attempt.student_id != best_match.student_id
    ):
        new_attempt.status = "FLAGGED"
        return "FLAGGED", best_similarity, best_match.id

    return "INGESTED", best_similarity, None

