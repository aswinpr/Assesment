from app.main import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    db.session.execute(text("SELECT 1"))
    print("DB connection from Flask OK")
