from app.telemetry import create_request_id, create_session_id, log_event
from evals.test_cases import TEST_CASES
from evals.evaluator import evaluate_case


PASS_THRESHOLD = 80


def main():
    session_id = create_session_id()
    request_id = create_request_id()

    print("Running evaluation suite...\n")

    total_score = 0
    total_max = 0
    results = []

    for test in TEST_CASES:
        result = evaluate_case(test)

        print(f"Test: {result['id']}")
        print(f"Category: {result['category']}")
        print(f"Score: {result['score']}/{result['max_score']}")
        print(f"Answer: {result['answer']}")
        print("-" * 50)

        total_score += result["score"]
        total_max += result["max_score"]
        results.append(result)

        log_event(
            event_type="eval_case_result",
            session_id=session_id,
            request_id=create_request_id(),
            agent_name="Evaluation Framework",
            model_name="llama3.2:3b",
            status="success",
            data={
                "test_id": result["id"],
                "category": result["category"],
                "score": result["score"],
                "max_score": result["max_score"],
            },
        )

    final_percentage = round(total_score / total_max * 100, 2)

    status = "pass" if final_percentage >= PASS_THRESHOLD else "fail"

    print("\nFINAL SCORE:")
    print(f"{total_score} / {total_max}")
    print(f"Average: {final_percentage}%")
    print(f"Threshold: {PASS_THRESHOLD}%")
    print(f"Result: {status.upper()}")

    log_event(
        event_type="eval_suite_result",
        session_id=session_id,
        request_id=request_id,
        agent_name="Evaluation Framework",
        model_name="llama3.2:3b",
        status=status,
        data={
            "total_score": total_score,
            "total_max": total_max,
            "average_percent": final_percentage,
            "pass_threshold": PASS_THRESHOLD,
            "result": status,
            "test_count": len(results),
        },
    )


if __name__ == "__main__":
    main()
