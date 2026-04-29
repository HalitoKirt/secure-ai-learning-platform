from app.agents.security_agent import (
    run_security_agent,
    extract_risk_level,
    should_block_request,
)
from app.telemetry import create_session_id, elapsed_ms, log_event, start_timer
from app.rag.rag import load_documents, query_docs
from app.agents.tutor_agent import run_tutor_agent
from app.agents.quiz_agent import run_quiz_agent, parse_quiz_output
from app.agents.evaluator_agent import run_evaluator_agent


MODEL_NAME = "llama3.2:3b"


def main():
    session_id = create_session_id()

    print("Secure AI Learning Platform")
    print("RAG + Tutor + Quiz + Evaluator + Security + Telemetry enabled")

    load_documents()

    while True:
        mode = input("\nChoose mode: tutor, quiz, evaluate, or exit: ").lower()

        if mode == "exit":
            print("Goodbye.")
            break

        if mode not in ["tutor", "quiz", "evaluate"]:
            print("Please choose 'tutor', 'quiz', 'evaluate', or 'exit'.")
            continue

        if mode == "evaluate":
            question = input("Question: ")
            expected_answer = input("Expected answer: ")
            user_answer = input("Your answer: ")

            eval_timer = start_timer()
            feedback = run_evaluator_agent(question, expected_answer, user_answer)
            eval_latency = elapsed_ms(eval_timer)

            print("\nEvaluator Agent Feedback:")
            print(feedback)

            log_event(
                event_type="manual_evaluation",
                session_id=session_id,
                agent_name="Evaluator Agent",
                model_name=MODEL_NAME,
                latency_ms=eval_latency,
                data={
                    "question": question,
                    "user_answer": user_answer,
                },
            )
            continue

        user_input = input("Enter your topic or question: ")

        docs = query_docs(user_input)
        context = "\n".join(docs)

        security_timer = start_timer()
        security_review = run_security_agent(user_input, context)
        security_latency = elapsed_ms(security_timer)
        risk_level = extract_risk_level(security_review)

        print("\nSecurity Agent Review:")
        print(security_review)

        log_event(
            event_type="security_review",
            session_id=session_id,
            agent_name="Security Agent",
            model_name=MODEL_NAME,
            risk_level=risk_level,
            latency_ms=security_latency,
            data={
                "mode": mode,
                "input": user_input,
                "review": security_review,
            },
        )

        if should_block_request(risk_level):
            print("\nRequest blocked by Security Agent due to High risk.")

            log_event(
                event_type="blocked_request",
                session_id=session_id,
                agent_name="Security Agent",
                model_name=MODEL_NAME,
                risk_level=risk_level,
                status="blocked",
                data={
                    "mode": mode,
                    "input": user_input,
                    "review": security_review,
                },
            )
            continue

        if risk_level == "Medium":
            print("\nWarning: Security Agent marked this request as Medium risk. Proceeding with caution.")

        if mode == "tutor":
            tutor_timer = start_timer()
            answer = run_tutor_agent(user_input, context)
            tutor_latency = elapsed_ms(tutor_timer)

            print("\nTutor Agent Response:")
            print(answer)

            log_event(
                event_type="tutor_response",
                session_id=session_id,
                agent_name="Tutor Agent",
                model_name=MODEL_NAME,
                risk_level=risk_level,
                latency_ms=tutor_latency,
                data={
                    "question": user_input,
                    "retrieved_chunks": docs,
                },
            )

        if mode == "quiz":
            quiz_timer = start_timer()
            quiz_output = run_quiz_agent(user_input, context)
            quiz_latency = elapsed_ms(quiz_timer)

            question, expected_answer = parse_quiz_output(quiz_output)

            if not question or not expected_answer:
                print("\nQuiz Agent Output:")
                print(quiz_output)
                print("\nCould not parse quiz output. Try again.")

                log_event(
                    event_type="quiz_parse_error",
                    session_id=session_id,
                    agent_name="Quiz Agent",
                    model_name=MODEL_NAME,
                    risk_level=risk_level,
                    status="error",
                    latency_ms=quiz_latency,
                    data={
                        "topic": user_input,
                        "raw_output": quiz_output,
                    },
                )
                continue

            print("\nQuiz Question:")
            print(question)

            user_answer = input("\nYour answer: ")

            eval_timer = start_timer()
            feedback = run_evaluator_agent(
                question=question,
                expected_answer=expected_answer,
                user_answer=user_answer,
            )
            eval_latency = elapsed_ms(eval_timer)

            print("\nEvaluator Agent Feedback:")
            print(feedback)

            log_event(
                event_type="quiz_evaluation",
                session_id=session_id,
                agent_name="Evaluator Agent",
                model_name=MODEL_NAME,
                risk_level=risk_level,
                latency_ms=eval_latency,
                data={
                    "topic": user_input,
                    "question": question,
                    "user_answer": user_answer,
                    "retrieved_chunks": docs,
                },
            )


if __name__ == "__main__":
    main()
