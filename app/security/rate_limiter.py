import os
import time
from fastapi import Request, HTTPException

from app.telemetry.logger import log_event

RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "5"))

request_history = {}


def enforce_rate_limit(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()

    timestamps = request_history.get(client_ip, [])

    timestamps = [
        timestamp for timestamp in timestamps
        if now - timestamp < RATE_LIMIT_WINDOW_SECONDS
    ]

    if len(timestamps) >= RATE_LIMIT_MAX_REQUESTS:
        log_event(
            "rate_limit_exceeded",
            {
                "client_ip": client_ip,
                "window_seconds": RATE_LIMIT_WINDOW_SECONDS,
                "max_requests": RATE_LIMIT_MAX_REQUESTS,
                "request_count": len(timestamps)
            }
        )

        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )

    timestamps.append(now)
    request_history[client_ip] = timestamps

    log_event(
        "rate_limit_checked",
        {
            "client_ip": client_ip,
            "window_seconds": RATE_LIMIT_WINDOW_SECONDS,
            "max_requests": RATE_LIMIT_MAX_REQUESTS,
            "request_count": len(timestamps),
            "status": "allowed"
        }
    )
