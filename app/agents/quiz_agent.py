import ollama


MODEL_NAME = "llama3.2:3b"


def run_quiz_agent(topic: str, context: str) -> str:
    """
    Quiz Agent:
    Creates practice questions using retrieved RAG context.
    """

    prompt = f"""
You are the Quiz Agent for the Secure AI Learning Platform.

Rules:
- Use the provided context first.
- Create 3 practice questions.
- Include the correct answer after each question.
- Keep explanations short and clear.
- Do not make up facts.
- If the context is not enough, say so.

Context:
{context}

Quiz Topic:
{topic}

Quiz Agent Output:
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]
