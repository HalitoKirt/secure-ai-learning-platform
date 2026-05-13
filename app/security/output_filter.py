import re
from typing import Dict, Any


SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",
    r"aws_secret_access_key",
    r"secret_access_key",
    r"api[_-]?key",
    r"password\s*[:=]",
    r"token\s*[:=]",
    r"bearer\s+[a-zA-Z0-9._\-]+"
]


SYSTEM_LEAK_PATTERNS = [
    r"system prompt",
    r"hidden instructions",
    r"developer instructions",
    r"internal policy",
    r"confidential instructions",
    r"you are chatgpt",
    r"you are an ai assistant"
]


def inspect_model_output(answer: str) -> Dict[str, Any]:
    """
    Inspect model output before returning it to the user.
    This acts as an output guardrail.
    """

    normalized_answer = answer.lower()

    matched_rules = []

    for pattern in SECRET_PATTERNS:
        if re.search(pattern, answer, re.IGNORECASE):
            matched_rules.append(pattern)

    for pattern in SYSTEM_LEAK_PATTERNS:
        if re.search(pattern, normalized_answer, re.IGNORECASE):
            matched_rules.append(pattern)

    if matched_rules:
        return {
            "allowed": False,
            "risk_level": "high",
            "action": "block",
            "reason": "unsafe_model_output_detected",
            "matched_rules": matched_rules
        }

    return {
        "allowed": True,
        "risk_level": "low",
        "action": "allow",
        "reason": "output_passed_safety_check",
        "matched_rules": []
    }
