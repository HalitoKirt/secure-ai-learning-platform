# Secure AI Learning Platform – Architecture

## 1. Purpose

The Secure AI Learning Platform is a hybrid, local-first AI security learning system designed to demonstrate secure AI architecture, RAG, multi-agent workflows, telemetry, evaluation, and future cloud integration.

The platform is built to show how AI systems can be:

- grounded in trusted knowledge
- protected by security controls
- evaluated for quality
- logged for observability
- designed for future AWS deployment

---

## 2. Current Architecture

```text
User
 │
 ▼
CLI Application
 │
 ▼
Request Router
 │
 ├── Tutor Mode
 │
 ├── Quiz Mode
 │
 ├── Evaluate Mode
 │
 └── PQC Mode
 │
 ▼
RAG Pipeline
 │
 ├── AWS Security Notes
 │
 ├── Chunking
 │
 ├── Embeddings
 │
 └── ChromaDB Vector Store
 │
 ▼
Security Agent
 │
 ├── Prompt risk review
 │
 ├── Risk classification
 │
 └── High-risk blocking
 │
 ▼
Agent Workflow
 │
 ├── Tutor Agent
 │
 ├── Quiz Agent
 │
 ├── Evaluator Agent
 │
 └── PQC Agent
 │
 ▼
Telemetry + Evaluation Logs
