import os

from fastapi import Header, HTTPException

from app.telemetry.logger import log_event


def validate_api_key(x_api_key: str = Header(None)):
    api_key = os.getenv("SECURE_API_KEY")

    if not api_key:
        log_event(
            "authentication_configuration_error",
            {
                "reason": "secure_api_key_not_configured"
            }
        )

        raise HTTPException(
            status_code=500,
            detail="Authentication service is not configured"
        )

    if x_api_key != api_key:
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
