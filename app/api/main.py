from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
import uuid
import time

from app.security.rate_limiter import enforce_rate_limit
from app.security.auth import validate_api_key
from app.security.detector import detect_prompt_injection, get_policy_action
from app.security.output_filter import inspect_model_output
from app.security.context_filter import inspect_retrieved_context

from app.agents.tutor_agent import run_tutor_agent
from app.agents.quiz_agent import run_quiz_agent
from app.agents.security_agent import run_security_agent
from app.agents.pqc_agent import run_pqc_agent
from app.agents.evaluator_agent import run_evaluator_agent

from app.rag.rag import query_docs

from app.telemetry.tracing import create_trace_id, create_span_id
from app.telemetry.logger import log_event


app = FastAPI(title="Secure AI Learning Platform API")


class AskRequest(BaseModel):
    question: str
    mode: str = "tutor"
    expected_answer: str | None = None
    user_answer: str | None = None


@app.get("/")
def root():
    return {"message": "Secure AI Learning Platform API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(
    request: AskRequest,
    http_request: Request,
    _: str = Depends(validate_api_key)
):
    enforce_rate_limit(http_request)

    mode = request.mode.lower().strip()
    request_id = str(uuid.uuid4())
    trace_id = create_trace_id()
    request_span_id = create_span_id("request")
    start_time = time.time()

    log_event("request_received", {
        "request_id": request_id,
        "trace_id": trace_id,
        "span_id": request_span_id,
        "component": "api",
        "endpoint": "/ask",
        "mode": mode,
        "status": "received"
    })

    try:
        security_detection = detect_prompt_injection(request.question)

        log_event("security_inspection_completed", {
            "request_id": request_id,
            "trace_id": trace_id,
            "span_id": create_span_id("security-inspection"),
            "component": "security",
            "endpoint": "/ask",
            "mode": mode,
            "is_suspicious": security_detection["is_suspicious"],
            "risk_level": security_detection["risk_level"],
            "risk_score": security_detection["risk_score"],
            "threat_type": security_detection["threat_type"],
            "detection_engine": security_detection["detection_engine"],
            "matches": security_detection["matches"]
        })

        policy_action = get_policy_action(security_detection["risk_level"])

        log_event("policy_action_applied", {
            "request_id": request_id,
            "trace_id": trace_id,
            "span_id": create_span_id("policy-action"),
            "component": "policy",
            "endpoint": "/ask",
            "mode": mode,
            "risk_level": security_detection["risk_level"],
            "risk_score": security_detection["risk_score"],
            "threat_type": security_detection["threat_type"],
            "detection_engine": security_detection["detection_engine"],
            "policy_action": policy_action,
            "policy_decision": policy_action,
            "matches": security_detection["matches"]
        })

        if policy_action == "block":
            log_event("request_blocked", {
                "request_id": request_id,
                "trace_id": trace_id,
                "span_id": create_span_id("request-blocked"),
                "component": "security",
                "endpoint": "/ask",
                "mode": mode,
                "status": "blocked",
                "reason": "high_risk_prompt_injection",
                "matches": security_detection["matches"]
            })

            raise HTTPException(
                status_code=403,
                detail="Request blocked by security policy."
            )

        retrieved_chunks = query_docs(request.question, n_results=3)

        log_event("rag_query_completed", {
            "request_id": request_id,
            "trace_id": trace_id,
            "span_id": create_span_id("rag-query"),
            "component": "rag",
            "endpoint": "/ask",
            "mode": mode,
            "chunks_retrieved": len(retrieved_chunks)
        })

        context_review = inspect_retrieved_context(retrieved_chunks)

        log_event("context_inspection_completed", {
            "request_id": request_id,
            "trace_id": trace_id,
            "span_id": create_span_id("context-inspection"),
            "component": "context_guardrail",
            "endpoint": "/ask",
            "mode": mode,
            "risk_level": context_review["risk_level"],
            "action": context_review["action"],
            "reason": context_review["reason"],
            "chunks_inspected": context_review["chunks_inspected"],
            "unsafe_chunk_count": context_review["unsafe_chunk_count"],
            "unsafe_chunks": context_review["unsafe_chunks"]
        })

        if not context_review["allowed"]:
            log_event("request_blocked", {
                "request_id": request_id,
                "trace_id": trace_id,
                "span_id": create_span_id("context-blocked"),
                "component": "context_guardrail",
                "endpoint": "/ask",
                "mode": mode,
                "status": "blocked",
                "reason": context_review["reason"],
                "unsafe_chunks": context_review["unsafe_chunks"]
            })

            raise HTTPException(
                status_code=403,
                detail="Request blocked because retrieved context failed safety inspection."
            )

        context = "\n\n".join(context_review["safe_chunks"])

        agent_start_time = time.time()

        if mode == "tutor":
            agent_name = "tutor"

            log_event("agent_selected", {
                "request_id": request_id,
                "trace_id": trace_id,
                "span_id": create_span_id("tutor-agent-selected"),
                "component": "agent",
                "endpoint": "/ask",
                "agent": agent_name,
                "mode": mode
            })

            answer = run_tutor_agent(
                question=request.question,
                context=context
            )

        elif mode == "quiz":
            agent_name = "quiz"

            log_event("agent_selected", {
                "request_id": request_id,
                "trace_id": trace_id,
                "span_id": create_span_id("quiz-agent-selected"),
                "component": "agent",
                "endpoint": "/ask",
                "agent": agent_name,
                "mode": mode
            })

            answer = run_quiz_agent(
                topic=request.question,
                context=context
            )

        elif mode == "security":
            agent_name = "security"

            log_event("agent_selected", {
                "request_id": request_id,
                "trace_id": trace_id,
                "span_id": create_span_id("security-agent-selected"),
                "component": "agent",
                "endpoint": "/ask",
                "agent": agent_name,
                "mode": mode
            })

            answer = run_security_agent(
                user_input=request.question,
                context=context
            )

        elif mode == "pqc":
            agent_name = "pqc"

            log_event("agent_selected", {
                "request_id": request_id,
                "trace_id": trace_id,
                "span_id": create_span_id("pqc-agent-selected"),
                "component": "agent",
                "endpoint": "/ask",
                "agent": agent_name,
                "mode": mode
            })

            answer = run_pqc_agent(
                user_input=request.question
            )

        elif mode == "evaluator":
            agent_name = "evaluator"

            log_event("agent_selected", {
                "request_id": request_id,
                "trace_id": trace_id,
                "span_id": create_span_id("evaluator-agent-selected"),
                "component": "agent",
                "endpoint": "/ask",
                "agent": agent_name,
                "mode": mode
            })

            if not request.expected_answer or not request.user_answer:
                raise HTTPException(
                    status_code=400,
                    detail="Evaluator mode requires expected_answer and user_answer."
                )

            answer = run_evaluator_agent(
                question=request.question,
                expected_answer=request.expected_answer,
                user_answer=request.user_answer
            )

        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid mode. Use tutor, quiz, security, pqc, or evaluator."
            )

        output_review = inspect_model_output(answer)

        log_event("output_inspection_completed", {
            "request_id": request_id,
            "trace_id": trace_id,
            "span_id": create_span_id("output-inspection"),
            "component": "output_guardrail",
            "endpoint": "/ask",
            "mode": mode,
            "risk_level": output_review["risk_level"],
            "action": output_review["action"],
            "reason": output_review["reason"],
            "matched_rules": output_review["matched_rules"]
        })

        if not output_review["allowed"]:
            log_event("response_blocked", {
                "request_id": request_id,
                "trace_id": trace_id,
                "span_id": create_span_id("response-blocked"),
                "component": "output_guardrail",
                "endpoint": "/ask",
                "mode": mode,
                "status": "blocked",
                "reason": output_review["reason"],
                "matched_rules": output_review["matched_rules"]
            })

            raise HTTPException(
                status_code=500,
                detail="Response blocked by output safety policy."
            )

        agent_duration_ms = round((time.time() - agent_start_time) * 1000, 2)

        log_event("agent_completed", {
            "request_id": request_id,
            "trace_id": trace_id,
            "span_id": create_span_id(f"{agent_name}-agent-completed"),
            "component": "agent",
            "endpoint": "/ask",
            "agent": agent_name,
            "mode": mode,
            "status": "success",
            "agent_duration_ms": agent_duration_ms
        })

        total_duration_ms = round((time.time() - start_time) * 1000, 2)

        log_event("request_completed", {
            "request_id": request_id,
            "trace_id": trace_id,
            "span_id": create_span_id("request-completed"),
            "component": "api",
            "endpoint": "/ask",
            "mode": mode,
            "status": "success",
            "duration_ms": total_duration_ms
        })

        return {
            "question": request.question,
            "mode": mode,
            "answer": answer
        }

    except HTTPException as e:
        log_event("request_failed", {
            "request_id": request_id,
            "trace_id": trace_id,
            "span_id": create_span_id("request-failed"),
            "component": "api",
            "endpoint": "/ask",
            "mode": mode,
            "status": "client_error",
            "error_type": type(e).__name__,
            "status_code": e.status_code
        })
        raise e

    except Exception as e:
        log_event("request_failed", {
            "request_id": request_id,
            "trace_id": trace_id,
            "span_id": create_span_id("request-failed"),
            "component": "api",
            "endpoint": "/ask",
            "mode": mode,
            "status": "server_error",
            "error_type": type(e).__name__
        })

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
