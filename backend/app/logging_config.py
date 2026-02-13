import logging
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "channel": getattr(record, "channel", "app"),
            "context": getattr(record, "context", {}),
            "extra": getattr(record, "extra_data", {})
        }

        return json.dumps(log_record)


def setup_logging(app):
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    app.logger.handlers = []
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    # Disable default werkzeug logs
    logging.getLogger("werkzeug").handlers = []
    logging.getLogger("werkzeug").propagate = False
