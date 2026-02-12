from app.models.attempt_score import AttemptScore
from app.extensions import db


def score_attempt(attempt):

    test = attempt.test

    existing = AttemptScore.query.filter_by(
        attempt_id=attempt.id
    ).first()

    if existing:
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

    return score
