import ollama

def main():
    print("Secure AI Learning Platform")
    print("Local LLM connected (Ollama)")

    while True:
        user_input = input("\nAsk a question or type 'exit': ")

        if user_input.lower() == "exit":
            print("Goodbye.")
            break

        response = ollama.chat(
            model="llama3.2:3b",
            messages=[{"role": "user", "content": user_input}]
        )

        print("\nAI Response:")
        print(response["message"]["content"])


if __name__ == "__main__":
    main()
