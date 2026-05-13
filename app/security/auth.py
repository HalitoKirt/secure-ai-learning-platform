import os
from fastapi import Header, HTTPException

from app.telemetry.logger import log_event

API_KEY = os.getenv("SECURE_API_KEY", "dev-secret-key")


def validate_api_key(x_api_key: str = Header(None)):

    if x_api_key != API_KEY:

        log_event(
            "authentication_failed",
            {
                "reason": "invalid_api_key"
            }
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )

    log_event(
        "authentication_succeeded",
        {}
    )
