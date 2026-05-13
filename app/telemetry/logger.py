import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict


logger = logging.getLogger("secure-ai-platform")
logger.setLevel(logging.INFO)


# Prevent duplicate handlers during FastAPI reloads
if not logger.handlers:

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler("logs/audit.log")
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(message)s")

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


def log_event(event_type: str, data: Dict[str, Any]) -> None:
    """
    Writes structured JSON telemetry events.
    Avoid logging secrets, tokens, credentials,
    or full sensitive prompts/responses.
    """

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "service": "secure-ai-learning-platform",
        "data": data
    }

    logger.info(json.dumps(event))
