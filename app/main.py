def main():
    print("Secure AI Learning Platform")
    print("Phase 1: Basic local application is running.")

    while True:
        user_input = input("\nAsk a question or type 'exit': ")

        if user_input.lower() == "exit":
            print("Goodbye.")
            break

        print(f"\nYou asked: {user_input}")
        print("AI response will be added in the next phase.")


if __name__ == "__main__":
    main()
