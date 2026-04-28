import ollama
from app.rag.rag import load_documents, query_docs

def main():
    print("Secure AI Learning Platform with RAG")

    load_documents()

    while True:
        user_input = input("\nAsk a question or type 'exit': ")

        if user_input.lower() == "exit":
            break

        docs = query_docs(user_input)

        context = "\n".join(docs)

        prompt = f"""
Use the following context to answer the question:

{context}

Question:
{user_input}
"""

        response = ollama.chat(
            model="llama3.2:3b",
            messages=[{"role": "user", "content": prompt}]
        )

        print("\nAI Response:")
        print(response["message"]["content"])

if __name__ == "__main__":
    main()
