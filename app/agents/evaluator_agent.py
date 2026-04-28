import ollama


MODEL_NAME = "llama3.2:3b"


def run_evaluator_agent(question: str, expected_answer: str, user_answer: str) -> str:
    """
    Evaluator Agent:
    Grades a user's answer against an expected answer.
    """

    prompt = f"""
You are the Evaluator Agent for the Secure AI Learning Platform.

Rules:
- Grade the user's answer against the expected answer.
- Give a score from 0 to 10.
- Explain what was correct.
- Explain what was missing or incorrect.
- Provide a stronger version of the answer.
- Keep feedback clear and encouraging.

Question:
{question}

Expected Answer:
{expected_answer}

User Answer:
{user_answer}

Evaluator Agent Feedback:
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]
