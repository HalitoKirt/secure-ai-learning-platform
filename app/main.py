from app.rag.rag import load_documents, query_docs
from app.agents.tutor_agent import run_tutor_agent
from app.agents.quiz_agent import run_quiz_agent, parse_quiz_output
from app.agents.evaluator_agent import run_evaluator_agent


def main():
    print("Secure AI Learning Platform")
    print("RAG + Tutor Agent + Interactive Quiz + Evaluator Agent enabled")

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

            feedback = run_evaluator_agent(question, expected_answer, user_answer)

            print("\nEvaluator Agent Feedback:")
            print(feedback)
            continue

        user_input = input("Enter your topic or question: ")

        docs = query_docs(user_input)
        context = "\n".join(docs)

        if mode == "tutor":
            answer = run_tutor_agent(user_input, context)
            print("\nTutor Agent Response:")
            print(answer)

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


if __name__ == "__main__":
    main()
