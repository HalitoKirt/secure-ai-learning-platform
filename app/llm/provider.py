import os
import ollama
import boto3

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-lite-v1:0")


def _to_bedrock_messages(messages: list[dict]) -> list[dict]:
    return [
        {
            "role": message.get("role", "user"),
            "content": [{"text": message.get("content", "")}],
        }
        for message in messages
    ]


def chat(messages: list[dict]) -> str:
    """
    Central LLM provider router.

    Local/dev:
      LLM_PROVIDER=ollama

    AWS/prod:
      LLM_PROVIDER=bedrock
    """

    if LLM_PROVIDER == "ollama":
        client = ollama.Client(host=OLLAMA_HOST)
        response = client.chat(
            model=OLLAMA_MODEL,
            messages=messages,
        )
        return response["message"]["content"]

    if LLM_PROVIDER == "bedrock":
        client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
        response = client.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=_to_bedrock_messages(messages),
            inferenceConfig={
                "maxTokens": 500,
                "temperature": 0.2,
            },
        )
        return response["output"]["message"]["content"][0]["text"]

    raise ValueError(f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}")
