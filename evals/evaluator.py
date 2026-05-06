from app.agents.tutor_agent import run_tutor_agent


def score_answer(answer: str, expected: str, required_terms: list[str] | None = None) -> dict:
    """
    Enterprise-style scoring function.

    Scores based on:
    - Accuracy (keyword match)
    - Clarity (length)
    - Directness (no deflection)
    - Required concept enforcement (PQC, etc.)
    """

    answer_lower = answer.lower()
    expected_lower = expected.lower()

    score = 0

    # -------------------------
    # 1. Accuracy (keyword match)
    # -------------------------
    expected_words = expected_lower.split()
    matches = sum(1 for word in expected_words if word in answer_lower)

    if matches >= 4:
        score += 4
    elif matches >= 2:
        score += 2

    # -------------------------
    # 2. Clarity (reasonable explanation length)
    # -------------------------
    if len(answer.split()) > 8:
        score += 2

    # -------------------------
    # 3. Directness (penalize deflection)
    # -------------------------
    if (
        "i need more context" not in answer_lower
        and "could you please provide" not in answer_lower
    ):
        score += 2

    # -------------------------
    # 4. Required concept enforcement (CRITICAL)
    # -------------------------
    if required_terms:
        required_matches = sum(
            1 for term in required_terms if term.lower() in answer_lower
        )

        # Strong match
        if required_matches >= len(required_terms) - 1:
            score += 2

        # Partial match
        elif required_matches >= 3:
            score += 1

        # Weak match → HARD CAP
        else:
            score = min(score, 5)

    # -------------------------
    # 5. Normalize score (0–10)
    # -------------------------
    score = max(0, min(score, 10))

    return {
        "score": score,
        "max_score": 10,
    }


def evaluate_case(test_case):
    """
    Runs a single test case through the system and evaluates it.
    """

    answer = run_tutor_agent(test_case["question"], context="")

    scoring = score_answer(
        answer,
        test_case["expected_answer"],
        test_case.get("required_terms"),
    )

    return {
        "id": test_case["id"],
        "question": test_case["question"],
        "answer": answer,
        "score": scoring["score"],
        "max_score": scoring["max_score"],
        "category": test_case["category"],
    }
