from app.llm.provider import chat


def run_tutor_agent(question: str, context: str) -> str:
    """
    Tutor Agent:
    Explains concepts using retrieved RAG context.
    """

    prompt = f"""
You are the Tutor Agent for the Secure AI Learning Platform.

Rules:
- Use the provided context first.
- Explain clearly and simply.
- Do not make up facts.
- If the context does not contain enough information, say so.
- Use examples when helpful.

Context:
{context}

User Question:
{question}

Tutor Agent Response:
"""

    return chat(
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
