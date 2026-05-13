TEST_CASES = [
    {
        "id": "cloudtrail_basic",
        "question": "What does AWS CloudTrail do?",
        "expected_answer": "Records AWS API activity for auditing and security monitoring.",
        "category": "security_logging",
    },
    {
        "id": "least_privilege",
        "question": "What is least privilege?",
        "expected_answer": "Only granting permissions required to perform a task.",
        "category": "iam",
    },
    {
    "id": "pqc_risk",
    "question": "Why is RSA risky for long-term sensitive data?",
    "expected_answer": "Quantum computers may break RSA in the future, creating harvest-now-decrypt-later risk for data that needs long-term confidentiality.",
    "category": "pqc",
    "required_terms": [
        "quantum",
        "rsa",
        "harvest",
        "decrypt",
        "long-term",
        "confidentiality",
    ],
  }
]
