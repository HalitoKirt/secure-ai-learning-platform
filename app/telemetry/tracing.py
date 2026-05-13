import uuid
import time


def create_trace_id() -> str:
    return str(uuid.uuid4())


def create_span_id(name: str) -> str:
    unique_id = str(uuid.uuid4())[:8]
    return f"{name}-{unique_id}"


def now_ms() -> float:
    return time.time()


def duration_ms(start_time: float) -> float:
    return round((time.time() - start_time) * 1000, 2)
