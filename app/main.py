from app.rag.rag import load_documents, query_docs
from app.agents.tutor_agent import run_tutor_agent


def main():
    print("Secure AI Learning Platform")
    print("RAG + Tutor Agent enabled")

    load_documents()

    while True:
        user_input = input("\nAsk a question or type 'exit': ")

        if user_input.lower() == "exit":
            print("Goodbye.")
            break

        docs = query_docs(user_input)
        context = "\n".join(docs)

        answer = run_tutor_agent(user_input, context)

        print("\nTutor Agent Response:")
        print(answer)


if __name__ == "__main__":
    main()
