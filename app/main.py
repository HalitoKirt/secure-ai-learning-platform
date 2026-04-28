from app.agents.security_agent import (
    run_security_agent,
    extract_risk_level,
    should_block_request,
)
from app.telemetry import log_event
from app.rag.rag import load_documents, query_docs
from app.agents.tutor_agent import run_tutor_agent
from app.agents.quiz_agent import run_quiz_agent, parse_quiz_output
from app.agents.evaluator_agent import run_evaluator_agent


def main():
    print("Secure AI Learning Platform")
    print("RAG + Tutor + Quiz + Evaluator + Telemetry enabled")

    load_documents()

    while True:
        mode = input("\nChoose mode: tutor, quiz, evaluate, or exit: ").lower()

        if mode == "exit":
            print("Goodbye.")
            break

        if mode not in ["tutor", "quiz", "evaluate"]:
            print("Please choose 'tutor', 'quiz', 'evaluate', or 'exit'.")
            continue

        # -------------------------
        # MANUAL EVALUATE MODE
        # -------------------------
        if mode == "evaluate":
            question = input("Question: ")
            expected_answer = input("Expected answer: ")
            user_answer = input("Your answer: ")

            feedback = run_evaluator_agent(question, expected_answer, user_answer)

            print("\nEvaluator Agent Feedback:")
            print(feedback)

            # ✅ TELEMETRY HERE
            log_event("manual_evaluation", {
                "question": question,
                "user_answer": user_answer,
            })

            continue

        # -------------------------
        # COMMON INPUT (tutor/quiz)
        # -------------------------
        user_input = input("Enter your topic or question: ")

        docs = query_docs(user_input)
        context = "\n".join(docs)

        security_review = run_security_agent(user_input, context)
        risk_level = extract_risk_level(security_review)

        print("\nSecurity Agent Review:")
        print(security_review)

        log_event("security_review", {
            "mode": mode,
            "input": user_input,
            "risk_level": risk_level,
            "review": security_review,
        })

        if should_block_request(risk_level):
            print("\nRequest blocked by Security Agent due to High risk.")
            log_event("blocked_request", {
                "mode": mode,
                "input": user_input,
                "risk_level": risk_level,
                "review": security_review,
            })
            continue

        if risk_level == "Medium":
            print("\nWarning: Security Agent marked this request as Medium risk. Proceeding with caution.")

        # -------------------------
        # TUTOR MODE
        # -------------------------
        if mode == "tutor":
            answer = run_tutor_agent(user_input, context)

            print("\nTutor Agent Response:")
            print(answer)

            # ✅ TELEMETRY HERE
            log_event("tutor_response", {
                "question": user_input,
                "retrieved_chunks": docs,
            })

        # -------------------------
        # QUIZ MODE (interactive)
        # -------------------------
        if mode == "quiz":
            quiz_output = run_quiz_agent(user_input, context)
            question, expected_answer = parse_quiz_output(quiz_output)

            if not question or not expected_answer:
                print("\nQuiz Agent Output:")
                print(quiz_output)
                print("\nCould not parse quiz output. Try again.")
                continue

            print("\nQuiz Question:")
            print(question)

            user_answer = input("\nYour answer: ")

            feedback = run_evaluator_agent(
                question=question,
                expected_answer=expected_answer,
                user_answer=user_answer
            )

            print("\nEvaluator Agent Feedback:")
            print(feedback)

            # ✅ TELEMETRY HERE
            log_event("quiz_evaluation", {
                "topic": user_input,
                "question": question,
                "user_answer": user_answer,
                "retrieved_chunks": docs,
            })


if __name__ == "__main__":
    main()
