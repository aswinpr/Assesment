from datetime import timedelta


def flag_attempt(attempt, similarity=None):
    """
    Apply fraud / anomaly detection rules.
    Returns: (is_flagged, reasons)
    """

    reasons = []

    # Suspiciously short duration 
    if attempt.started_at and attempt.submitted_at:
        duration = attempt.submitted_at - attempt.started_at

        # configurable threshold (example: 5 minutes)
        if duration < timedelta(minutes=5):
            reasons.append("SUSPICIOUS_DURATION")

    # Perfect score anomaly ----
    if attempt.score:
        score = attempt.score

        if score.correct == score.total_questions and score.total_questions > 0:
            reasons.append("PERFECT_SCORE")

    # High similarity but not deduped 
    if similarity and similarity > 0.95:
        reasons.append("HIGH_SIMILARITY_PATTERN")

    is_flagged = len(reasons) > 0

    return is_flagged, reasons
