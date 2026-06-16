from collections.abc import Callable
from time import perf_counter
from typing import Any

from sqlalchemy.orm import Session

from app.agents.state import ResearchGraphState
from app.models.common import utc_now
from app.models.research import AgentStep, AgentStepStatus, ResearchRun, ResearchRunStatus

NodeHandler = Callable[[ResearchGraphState], dict[str, Any]]


def record_agent_step(
    db: Session,
    run: ResearchRun,
    node_name: str,
    state: ResearchGraphState,
    handler: NodeHandler,
) -> dict[str, Any]:
    started_at = utc_now()
    step = AgentStep(
        run_id=run.id,
        node_name=node_name,
        input_payload=_snapshot_state(state),
        status=AgentStepStatus.RUNNING,
        started_at=started_at,
    )
    run.current_node = node_name
    db.add(step)
    db.commit()

    timer_started_at = perf_counter()
    try:
        output = handler(state)
    except Exception as exc:
        completed_at = utc_now()
        step.status = AgentStepStatus.FAILED
        step.completed_at = completed_at
        step.latency_ms = _elapsed_ms(timer_started_at)
        step.error_message = str(exc)
        run.status = ResearchRunStatus.FAILED
        run.error_message = str(exc)
        run.completed_at = completed_at
        db.commit()
        raise

    step.status = AgentStepStatus.COMPLETED
    step.output_payload = output
    step.completed_at = utc_now()
    step.latency_ms = _elapsed_ms(timer_started_at)
    db.commit()

    return output


def _elapsed_ms(started_at: float) -> int:
    return int((perf_counter() - started_at) * 1000)


def _snapshot_state(state: ResearchGraphState) -> dict[str, Any]:
    return {
        "run_id": state["run_id"],
        "query": state["query"],
        "quota_allowed": state["quota_allowed"],
        "plan_count": len(state["plan"]),
        "research_note_count": len(state["research_notes"]),
        "has_summary": bool(state["summary"]),
        "has_critique": bool(state["critique"]),
        "has_report": bool(state["report_markdown"]),
        "errors": state["errors"],
    }
