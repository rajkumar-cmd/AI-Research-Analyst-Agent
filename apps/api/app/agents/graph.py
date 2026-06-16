from collections.abc import Callable
from typing import Any

from langgraph.graph import END, START, StateGraph
from sqlalchemy.orm import Session

from app.agents.nodes import (
    critic_node,
    planner_node,
    quota_guard_node,
    report_writer_node,
    research_node,
    summarizer_node,
)
from app.agents.providers import LLMProvider, MockLLMProvider
from app.agents.state import ResearchGraphState
from app.agents.step_recorder import record_agent_step
from app.models.common import utc_now
from app.models.research import ResearchRun, ResearchRunStatus

NodeFactory = Callable[[ResearchGraphState], dict[str, Any]]


def build_research_graph(
    db: Session | None = None,
    run: ResearchRun | None = None,
    provider: LLMProvider | None = None,
):
    provider = provider or MockLLMProvider()
    workflow = StateGraph(ResearchGraphState)

    workflow.add_node("quota_guard", _node(db, run, "quota_guard", quota_guard_node))
    workflow.add_node("planner_agent", _node(db, run, "planner_agent", lambda state: planner_node(state, provider)))
    workflow.add_node("research_agent", _node(db, run, "research_agent", lambda state: research_node(state, provider)))
    workflow.add_node("summarizer_agent", _node(db, run, "summarizer_agent", lambda state: summarizer_node(state, provider)))
    workflow.add_node("critic_agent", _node(db, run, "critic_agent", lambda state: critic_node(state, provider)))
    workflow.add_node("report_writer_agent", _node(db, run, "report_writer_agent", lambda state: report_writer_node(state, provider)))

    workflow.add_edge(START, "quota_guard")
    workflow.add_edge("quota_guard", "planner_agent")
    workflow.add_edge("planner_agent", "research_agent")
    workflow.add_edge("research_agent", "summarizer_agent")
    workflow.add_edge("summarizer_agent", "critic_agent")
    workflow.add_edge("critic_agent", "report_writer_agent")
    workflow.add_edge("report_writer_agent", END)

    return workflow.compile()


def run_research_workflow(
    db: Session,
    run: ResearchRun,
    provider: LLMProvider | None = None,
) -> ResearchGraphState:
    run.status = ResearchRunStatus.RUNNING
    run.started_at = run.started_at or utc_now()
    run.error_message = None
    db.commit()

    graph = build_research_graph(db=db, run=run, provider=provider)
    state = _initial_state(run)

    try:
        final_state = graph.invoke(state)
    except Exception:
        db.refresh(run)
        raise

    run.status = ResearchRunStatus.COMPLETED
    run.current_node = "report_writer_agent"
    run.completed_at = utc_now()
    db.commit()

    return final_state


def _node(
    db: Session | None,
    run: ResearchRun | None,
    node_name: str,
    handler: NodeFactory,
) -> NodeFactory:
    if db is None or run is None:
        return handler

    def wrapped(state: ResearchGraphState) -> dict[str, Any]:
        return record_agent_step(db=db, run=run, node_name=node_name, state=state, handler=handler)

    return wrapped


def _initial_state(run: ResearchRun) -> ResearchGraphState:
    return {
        "run_id": run.id,
        "user_id": run.user_id,
        "query": run.query,
        "quota_allowed": False,
        "plan": [],
        "research_notes": [],
        "summary": "",
        "critique": "",
        "report_markdown": "",
        "errors": [],
    }
