import ollama


MODEL_NAME = "llama3.2:3b"


def run_pqc_agent(user_input: str) -> str:
    """
    PQC Agent:
    Reviews scenarios for post-quantum security risks.
    """

    prompt = f"""
You are the Post-Quantum Security Advisor.

Analyze the scenario for future quantum security risk.

You MUST consider and mention these concepts when relevant:
- quantum computers may break RSA or ECC in the future
- harvest-now-decrypt-later risk
- long-term confidentiality requirements
- crypto agility
- hybrid migration paths using classical + post-quantum approaches

If the scenario mentions RSA, ECC, TLS, certificates, encryption, long-term storage,
PII, regulated data, backups, logs, or customer data, explicitly evaluate whether
post-quantum risk applies.

Return your answer in this exact format:

RISK_LEVEL: Low / Medium / High

FINDINGS:
- <finding 1>
- <finding 2>
- <finding 3>

RECOMMENDATION:
- <action 1>
- <action 2>
- <action 3>

Scenario:
{user_input}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )

    return response["message"]["content"]
