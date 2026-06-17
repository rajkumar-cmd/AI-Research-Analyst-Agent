from typing import Any

from sqlalchemy.orm import Session

from app.agents.providers import LLMProvider, MockLLMProvider
from app.agents.state import ResearchGraphState
from app.agents.nodes import report_writer_node
from app.agents.step_recorder import record_agent_step
from app.models.common import utc_now
from app.models.research import ApprovalRequest, ApprovalStatus, ResearchRun, ResearchRunStatus


def approve_approval_request(
    db: Session,
    approval_request_id: str,
    reviewer_feedback: str | None = None,
) -> ApprovalRequest:
    approval_request = _get_approval_request(db, approval_request_id)
    approval_request.status = ApprovalStatus.APPROVED
    approval_request.reviewer_feedback = reviewer_feedback
    approval_request.approved_at = utc_now()

    run = _get_research_run(db, approval_request.run_id)
    run.status = ResearchRunStatus.RUNNING
    run.current_node = "report_writer_agent"
    db.commit()
    db.refresh(approval_request)
    return approval_request


def reject_approval_request(
    db: Session,
    approval_request_id: str,
    reviewer_feedback: str | None = None,
) -> ApprovalRequest:
    approval_request = _get_approval_request(db, approval_request_id)
    approval_request.status = ApprovalStatus.REJECTED
    approval_request.reviewer_feedback = reviewer_feedback

    run = _get_research_run(db, approval_request.run_id)
    run.status = ResearchRunStatus.CANCELLED
    run.error_message = reviewer_feedback or "Research run rejected during human approval."
    run.completed_at = utc_now()
    db.commit()
    db.refresh(approval_request)
    return approval_request


def request_approval_revision(
    db: Session,
    approval_request_id: str,
    reviewer_feedback: str,
) -> ApprovalRequest:
    approval_request = _get_approval_request(db, approval_request_id)
    approval_request.status = ApprovalStatus.REVISION_REQUESTED
    approval_request.reviewer_feedback = reviewer_feedback

    run = _get_research_run(db, approval_request.run_id)
    run.status = ResearchRunStatus.WAITING_FOR_APPROVAL
    run.current_node = "human_approval"
    db.commit()
    db.refresh(approval_request)
    return approval_request


def resume_approved_research_workflow(
    db: Session,
    approval_request_id: str,
    provider: LLMProvider | None = None,
) -> ResearchGraphState:
    provider = provider or MockLLMProvider()
    approval_request = _get_approval_request(db, approval_request_id)
    if approval_request.status != ApprovalStatus.APPROVED:
        raise ValueError("Only approved research runs can be resumed.")

    run = _get_research_run(db, approval_request.run_id)
    state = _state_from_approval_request(approval_request)
    state["approval_status"] = approval_request.status.value

    output = record_agent_step(
        db=db,
        run=run,
        node_name="report_writer_agent",
        state=state,
        handler=lambda current_state: report_writer_node(current_state, provider),
    )
    state.update(output)

    run.status = ResearchRunStatus.COMPLETED
    run.current_node = "report_writer_agent"
    run.completed_at = utc_now()
    db.commit()
    return state


def _get_approval_request(db: Session, approval_request_id: str) -> ApprovalRequest:
    approval_request = db.get(ApprovalRequest, approval_request_id)
    if approval_request is None:
        raise ValueError("Approval request not found.")

    return approval_request


def _get_research_run(db: Session, run_id: str) -> ResearchRun:
    run = db.get(ResearchRun, run_id)
    if run is None:
        raise ValueError("Research run not found.")

    return run


def _state_from_approval_request(approval_request: ApprovalRequest) -> ResearchGraphState:
    payload = approval_request.draft_payload or {}
    return {
        "run_id": _payload_str(payload, "run_id", approval_request.run_id),
        "user_id": _payload_str(payload, "user_id", approval_request.user_id),
        "query": _payload_str(payload, "query", ""),
        "quota_allowed": True,
        "approval_required": True,
        "approval_request_id": approval_request.id,
        "approval_status": approval_request.status.value,
        "plan": _payload_list(payload, "plan"),
        "research_notes": _payload_list(payload, "research_notes"),
        "summary": _payload_str(payload, "summary", ""),
        "critique": _payload_str(payload, "critique", ""),
        "report_markdown": "",
        "errors": [],
    }


def _payload_str(payload: dict[str, Any], key: str, default: str) -> str:
    value = payload.get(key, default)
    return value if isinstance(value, str) else default


def _payload_list(payload: dict[str, Any], key: str) -> list[str]:
    value = payload.get(key, [])
    if not isinstance(value, list):
        return []

    return [item for item in value if isinstance(item, str)]
