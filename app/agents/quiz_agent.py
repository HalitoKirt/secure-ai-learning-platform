import ollama


MODEL_NAME = "llama3.2:3b"


def run_quiz_agent(topic: str, context: str) -> str:
    """
    Quiz Agent:
    Creates one practice question and one expected answer using retrieved RAG context.
    """

    prompt = f"""
You are the Quiz Agent for the Secure AI Learning Platform.

Rules:
- Use the provided context first.
- Create exactly ONE practice question.
- Provide exactly ONE expected answer.
- Keep the question clear.
- Keep the expected answer concise.
- Do not make up facts.
- Use this exact format:

QUESTION:
<question here>

EXPECTED_ANSWER:
<expected answer here>

Context:
{context}

Quiz Topic:
{topic}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


def parse_quiz_output(quiz_output: str) -> tuple[str, str]:
    """
    Extract question and expected answer from Quiz Agent output.
    """

    question = ""
    expected_answer = ""

    if "QUESTION:" in quiz_output and "EXPECTED_ANSWER:" in quiz_output:
        question_part = quiz_output.split("QUESTION:", 1)[1]
        question = question_part.split("EXPECTED_ANSWER:", 1)[0].strip()
        expected_answer = question_part.split("EXPECTED_ANSWER:", 1)[1].strip()

    return question, expected_answer
