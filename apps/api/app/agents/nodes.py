from sqlalchemy.orm import Session

from app.agents.providers import LLMProvider
from app.agents.source_validation import (
    SourceValidationAgent,
    persist_source_validation_results,
    source_candidates_from_state,
)
from app.agents.state import ResearchGraphState
from app.models.research import ApprovalRequest, ApprovalStatus, ResearchRun


def quota_guard_node(state: ResearchGraphState) -> dict[str, object]:
    query = state["query"].strip()
    if not query:
        return {"quota_allowed": False, "errors": ["Research query cannot be empty."]}

    return {"quota_allowed": True}


def planner_node(state: ResearchGraphState, provider: LLMProvider) -> dict[str, object]:
    if not state["quota_allowed"]:
        return {"errors": [*state["errors"], "Planner skipped because quota guard failed."]}

    return {"plan": provider.plan(state["query"])}


def research_node(state: ResearchGraphState, provider: LLMProvider) -> dict[str, object]:
    return {"research_notes": provider.research(state["query"], state["plan"])}


def source_validation_node(
    state: ResearchGraphState,
    db: Session | None = None,
    run: ResearchRun | None = None,
    validator: SourceValidationAgent | None = None,
) -> dict[str, object]:
    validator = validator or SourceValidationAgent()
    candidates = source_candidates_from_state(state["source_candidates"])
    if not candidates:
        candidates = validator.build_candidates(state["query"], state["research_notes"])

    validation_results = validator.validate_many(candidates, state["query"])
    if db is not None and run is not None:
        persist_source_validation_results(db=db, run=run, results=validation_results)

    quality_score = 0.0
    if validation_results:
        quality_score = round(
            sum(result.credibility_score for result in validation_results) / len(validation_results),
            2,
        )

    return {
        "source_candidates": [candidate.__dict__ for candidate in candidates],
        "validated_sources": [result.to_state_payload() for result in validation_results],
        "source_quality_score": quality_score,
    }


def summarizer_node(state: ResearchGraphState, provider: LLMProvider) -> dict[str, object]:
    return {"summary": provider.summarize(state["query"], state["research_notes"])}


def critic_node(state: ResearchGraphState, provider: LLMProvider) -> dict[str, object]:
    return {"critique": provider.critique(state["summary"])}


def human_approval_node(
    state: ResearchGraphState,
    db: Session | None = None,
    run: ResearchRun | None = None,
) -> dict[str, object]:
    if not state["approval_required"]:
        return {"approval_status": "not_required"}

    if db is None or run is None:
        return {"approval_status": ApprovalStatus.PENDING.value}

    approval_request = ApprovalRequest(
        run_id=run.id,
        user_id=run.user_id,
        status=ApprovalStatus.PENDING,
        draft_payload={
            "run_id": state["run_id"],
            "user_id": state["user_id"],
            "query": state["query"],
            "plan": state["plan"],
            "research_notes": state["research_notes"],
            "source_candidates": state["source_candidates"],
            "validated_sources": state["validated_sources"],
            "source_quality_score": state["source_quality_score"],
            "summary": state["summary"],
            "critique": state["critique"],
        },
    )
    db.add(approval_request)
    db.flush()

    return {
        "approval_request_id": approval_request.id,
        "approval_status": approval_request.status.value,
    }


def report_writer_node(state: ResearchGraphState, provider: LLMProvider) -> dict[str, object]:
    return {
        "report_markdown": provider.write_report(
            query=state["query"],
            summary=state["summary"],
            critique=state["critique"],
        )
    }
