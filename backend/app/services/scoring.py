from app.models.attempt_score import AttemptScore
from app.extensions import db
from flask import current_app, g
import time


def score_attempt(attempt):

    start_time = time.time()
    test = attempt.test

    # Prevent double scoring
    existing = AttemptScore.query.filter_by(
        attempt_id=attempt.id
    ).first()

    if existing:
        return existing

    answers = attempt.answers or {}
    answer_key = test.answer_key or {}
    marking = test.negative_marking or {}

    # Extract marking safely
    correct_marks = float(marking.get("correct", 1))
    wrong_marks = float(marking.get("wrong", 0))
    skip_marks = float(marking.get("skip", 0))

    total_questions = len(answers)
    correct = 0
    incorrect = 0
    skipped = 0

    for q_id, answer in answers.items():

        if answer == "SKIP":
            skipped += 1
            continue

        correct_answer = answer_key.get(q_id)

        if correct_answer and answer == correct_answer:
            correct += 1
        else:
            incorrect += 1

    # ---- Required Metrics ----

    net_correct = correct - incorrect

    attempted = correct + incorrect
    accuracy = round((correct / attempted) * 100, 2) if attempted > 0 else 0.0

    final_score = (
        correct * correct_marks +
        incorrect * wrong_marks +
        skipped * skip_marks
    )

    negative_score = incorrect * abs(wrong_marks)

    # ---- Save Score ----

    score = AttemptScore(
        attempt_id=attempt.id,
        total_questions=total_questions,
        correct=correct,
        incorrect=incorrect,
        skipped=skipped,
        raw_score=correct,
        negative_score=negative_score,
        net_correct=net_correct,
        accuracy=accuracy,
        final_score=final_score,
        explanation={
            "formula": "correct*correct_marks + incorrect*wrong_marks + skipped*skip_marks",
            "negative_marking": marking
        }
    )

    db.session.add(score)
    attempt.status = "SCORED"
    db.session.flush()

    # ---- Structured Log ----

    duration = round((time.time() - start_time) * 1000, 2)

    current_app.logger.info(
        "Scoring completed",
        extra={
            "channel": "scoring",
            "context": {
                "request_id": getattr(g, "request_id", None),
                "attempt_id": str(attempt.id),
                "student_id": str(attempt.student_id)
            },
            "extra_data": {
                "correct": correct,
                "incorrect": incorrect,
                "skipped": skipped,
                "net_correct": net_correct,
                "accuracy": accuracy,
                "final_score": final_score,
                "duration_ms": duration
            }
        }
    )

    return score
