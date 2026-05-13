import re
from typing import Dict, Any, List


CONTEXT_INJECTION_PATTERNS = [
    r"ignore.*previous.*instructions",
    r"ignore.*all.*previous.*instructions",
    r"disregard.*previous.*instructions",
    r"forget.*previous.*instructions",
    r"override.*system.*instructions",
    r"reveal.*system.*prompt",
    r"show.*system.*prompt",
    r"print.*system.*prompt",
    r"disclose.*system.*prompt",
    r"bypass.*security",
    r"disable.*safety",
    r"developer.*mode",
    r"dan.*mode",
    r"you.*are.*now.*dan",
    r"act.*as.*system",
    r"act.*as.*developer",
    r"roleplay.*as.*system",
    r"roleplay.*as.*developer",
    r"pretend.*you.*are.*system",
    r"pretend.*you.*are.*developer"
]


def inspect_retrieved_context(chunks: List[str]) -> Dict[str, Any]:
    """
    Inspect RAG-retrieved chunks before they are sent to the model.
    This helps defend against indirect prompt injection.
    """

    unsafe_chunks = []
    safe_chunks = []

    for index, chunk in enumerate(chunks):
        matched_rules = []

        for pattern in CONTEXT_INJECTION_PATTERNS:
            if re.search(pattern, chunk, re.IGNORECASE):
                matched_rules.append(pattern)

        if matched_rules:
            unsafe_chunks.append({
                "chunk_index": index,
                "matched_rules": matched_rules
            })
        else:
            safe_chunks.append(chunk)

    if unsafe_chunks:
        return {
            "allowed": False,
            "risk_level": "high",
            "action": "block",
            "reason": "unsafe_retrieved_context_detected",
            "safe_chunks": safe_chunks,
            "unsafe_chunks": unsafe_chunks,
            "chunks_inspected": len(chunks),
            "unsafe_chunk_count": len(unsafe_chunks)
        }

    return {
        "allowed": True,
        "risk_level": "low",
        "action": "allow",
        "reason": "retrieved_context_passed_safety_check",
        "safe_chunks": safe_chunks,
        "unsafe_chunks": [],
        "chunks_inspected": len(chunks),
        "unsafe_chunk_count": 0
    }
