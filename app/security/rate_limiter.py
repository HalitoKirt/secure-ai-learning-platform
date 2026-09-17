import os
import time

from fastapi import HTTPException, Request

from app.telemetry.logger import log_event


RATE_LIMIT_WINDOW_SECONDS = int(
    os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60")
)
RATE_LIMIT_MAX_REQUESTS = int(
    os.getenv("RATE_LIMIT_MAX_REQUESTS", "5")
)

request_history = {}


def get_client_ip(request: Request) -> str:
    """
    Resolve the originating client address.

    AWS Application Load Balancer appends the client address to
    X-Forwarded-For. The first value represents the originating client.
    Local requests fall back to the direct connection address.

    The AWS deployment restricts direct ECS ingress to the ALB security
    group, which provides the proxy trust boundary for the deployed app.
    """
    forwarded_for = request.headers.get("x-forwarded-for")

    if forwarded_for:
        client_ip = forwarded_for.split(",", 1)[0].strip()

        if client_ip:
            return client_ip

    if request.client:
        return request.client.host

    return "unknown"


def enforce_rate_limit(request: Request):
    client_ip = get_client_ip(request)
    now = time.time()

    timestamps = request_history.get(client_ip, [])

    timestamps = [
        timestamp
        for timestamp in timestamps
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
