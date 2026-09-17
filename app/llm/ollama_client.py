import os
import ollama

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

client = ollama.Client(host=OLLAMA_HOST)
