from app.main import create_app
from app.extensions import db
from app.models.attempt import Attempt
from app.models.attempt_score import AttemptScore
from app.services.scoring import score_attempt

app = create_app()

with app.app_context():

    print("Deleting old scores...")
    AttemptScore.query.delete()
    db.session.commit()

    print("Recomputing all attempts...")

    attempts = Attempt.query.all()

    for attempt in attempts:
        score_attempt(attempt)

    db.session.commit()

print("✅ All attempts recomputed successfully.")
