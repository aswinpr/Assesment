from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate
from app import models
import time
import uuid
from flask import request, g
from app.logging_config import setup_logging


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    setup_logging(app) 

    @app.route("/")
    def index():
        return "Assessment API is running"

    db.init_app(app)
    migrate.init_app(app, db)


    @app.before_request
    def start_request():
        g.start_time = time.time()
        g.request_id = str(uuid.uuid4())

        app.logger.info(
            "Request started",
            extra={
                "channel": "http",
                "context": {
                    "request_id": g.request_id
                },
                "extra_data": {
                    "ip": request.remote_addr,
                    "user_agent": request.headers.get("User-Agent"),
                    "method": request.method,
                    "path": request.path,
                    "query_params": request.args.to_dict()
                }
            }
        )

    @app.after_request
    def end_request(response):
        latency = round((time.time() - g.start_time) * 1000, 2)

        app.logger.info(
            "Request completed",
            extra={
                "channel": "http",
                "context": {
                    "request_id": g.request_id
                },
                "extra_data": {
                    "status_code": response.status_code,
                    "latency_ms": latency
                }
            }
        )

        return response

    from .routes.health import bp as health_bp
    from .routes.ingest import bp as ingest_bp
    from .routes.analytics import bp as analytics_bp
    from app.routes.attempts import bp as attempts_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(ingest_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(attempts_bp)

    return app
