from datetime import datetime

def parse_iso_datetime(value: str):
    """
    Safely parse ISO datetime.
    Returns datetime or None if invalid.
    """
    if not value:
        return None

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None
