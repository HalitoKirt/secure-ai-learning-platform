from typing import Dict, Any
import json
import re
from pathlib import Path


POLICY_FILE = Path(__file__).parent / "policies.json"


def load_policies() -> dict:
    with open(POLICY_FILE, "r") as f:
        return json.load(f)


def normalize_text(text: str) -> str:
    return " ".join(text.lower().strip().split())


def find_matches(patterns: list[str], text: str) -> list[str]:
    matches = []

    for pattern in patterns:
        pattern_normalized = pattern.lower().strip()

        try:
            if re.search(pattern_normalized, text):
                matches.append(pattern)
        except re.error:
            if pattern_normalized in text:
                matches.append(pattern)

    return matches


def calculate_risk_score(risk_level: str, match_count: int) -> int:
    if risk_level == "high":
        return min(100, 90 + match_count)
    if risk_level == "medium":
        return min(89, 50 + match_count)
    return 0


def detect_prompt_injection(user_input: str) -> Dict[str, Any]:
    policies = load_policies()

    high_risk_patterns = policies.get("high_risk_patterns", [])
    medium_risk_patterns = policies.get("medium_risk_patterns", [])

    normalized_input = normalize_text(user_input)

    high_matches = find_matches(high_risk_patterns, normalized_input)
    medium_matches = find_matches(medium_risk_patterns, normalized_input)

    if high_matches:
        risk_level = "high"
        matches = high_matches
    elif medium_matches:
        risk_level = "medium"
        matches = medium_matches
    else:
        risk_level = "low"
        matches = []

    risk_score = calculate_risk_score(risk_level, len(matches))

    return {
        "is_suspicious": risk_level != "low",
        "risk_level": risk_level,
        "risk_score": risk_score,
        "threat_type": "prompt_injection" if risk_level != "low" else "none",
        "detection_engine": "regex_policy",
        "matches": matches
    }


def get_policy_action(risk_level: str) -> str:
    policies = load_policies()
    policy_actions = policies.get("policy_actions", {})

    return policy_actions.get(risk_level, "allow")
