from app.models.attempt_score import AttemptScore
from app.extensions import db
from flask import current_app, g
import time


def score_attempt(attempt):

    start_time = time.time()

    test = attempt.test

    existing = AttemptScore.query.filter_by(
        attempt_id=attempt.id
    ).first()

    if existing:
        current_app.logger.info(
            "Score already exists — skipping recompute",
            extra={
                "channel": "scoring",
                "context": {
                    "request_id": getattr(g, "request_id", None),
                    "attempt_id": str(attempt.id),
                    "student_id": str(attempt.student_id)
                },
                "extra_data": {
                    "final_score": existing.final_score
                }
            }
        )
        return existing

    answers = attempt.answers or {}
    answer_key = test.answer_key or {}

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

    raw_score = correct
    negative_score = incorrect * float(test.negative_marking)
    final_score = raw_score - negative_score

    score = AttemptScore(
        attempt_id=attempt.id,
        total_questions=total_questions,
        correct=correct,
        incorrect=incorrect,
        skipped=skipped,
        raw_score=raw_score,
        negative_score=negative_score,
        final_score=final_score,
        explanation={
            "formula": "correct - (incorrect * negative_marking)",
            "negative_marking": test.negative_marking
        }
    )

    db.session.add(score)
    attempt.status = "SCORED"
    db.session.flush()

    duration = round((time.time() - start_time) * 1000, 2)

    # ✅ Structured Scoring Log
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
                "total_questions": total_questions,
                "final_score": final_score,
                "duration_ms": duration
            }
        }
    )

    return score
