from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    @app.route("/")
    def index():
        return "Assessment API is running"

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.health import bp as health_bp
    app.register_blueprint(health_bp)

    return app
