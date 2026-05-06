from app.agents.evaluator_agent import run_evaluator_agent


TEST_CASES = [
    {
        "question": "What does AWS CloudTrail do?",
        "expected_answer": "AWS CloudTrail records AWS API activity and account events for auditing and security investigation.",
        "user_answer": "CloudTrail records API activity and account events.",
    },
    {
        "question": "What does least privilege mean?",
        "expected_answer": "Least privilege means giving only the permissions required to perform a task.",
        "user_answer": "It means only giving users the access they need.",
    },
]


def main():
    print("Running basic evals...\n")

    for index, test in enumerate(TEST_CASES, start=1):
        print(f"Eval {index}: {test['question']}")

        feedback = run_evaluator_agent(
            question=test["question"],
            expected_answer=test["expected_answer"],
            user_answer=test["user_answer"],
        )

        print(feedback)
        print("-" * 60)


if __name__ == "__main__":
    main()
