from app.rag.rag import load_documents, query_docs
from app.agents.tutor_agent import run_tutor_agent
from app.agents.quiz_agent import run_quiz_agent


def main():
    print("Secure AI Learning Platform")
    print("RAG + Tutor Agent + Quiz Agent enabled")

    load_documents()

    while True:
        mode = input("\nChoose mode: tutor, quiz, or exit: ").lower()

        if mode == "exit":
            print("Goodbye.")
            break

        if mode not in ["tutor", "quiz"]:
            print("Please choose 'tutor', 'quiz', or 'exit'.")
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
