from app.rag.rag import load_documents, query_docs
from app.agents.tutor_agent import run_tutor_agent
from app.agents.quiz_agent import run_quiz_agent
from app.agents.evaluator_agent import run_evaluator_agent


def main():
    print("Secure AI Learning Platform")
    print("RAG + Tutor Agent + Quiz Agent + Evaluator Agent enabled")

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
            quiz = run_quiz_agent(user_input, context)
            print("\nQuiz Agent Response:")
            print(quiz)


if __name__ == "__main__":
    main()
