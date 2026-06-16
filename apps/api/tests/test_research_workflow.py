from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agents.graph import run_research_workflow
from app.agents.providers import MockLLMProvider
from app.core.database import Base
from app.models.research import AgentStep, AgentStepStatus, ResearchRun, ResearchRunStatus
from app.models.user import User


def test_research_workflow_runs_langgraph_nodes_and_records_steps(db_session: Session) -> None:
    user = User(
        name="Rajkumar Pradhan",
        email="rajkumar.workflow@example.com",
        password_hash="hashed-password",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    run = ResearchRun(user_id=user.id, query="Research top AI data engineering trends for 2026")
    db_session.add(run)
    db_session.commit()
    db_session.refresh(run)

    final_state = run_research_workflow(db=db_session, run=run, provider=MockLLMProvider())

    db_session.refresh(run)
    steps = db_session.scalars(select(AgentStep).order_by(AgentStep.started_at)).all()

    assert run.status == ResearchRunStatus.COMPLETED
    assert run.current_node == "report_writer_agent"
    assert "Research Brief" in final_state["report_markdown"]
    assert [step.node_name for step in steps] == [
        "quota_guard",
        "planner_agent",
        "research_agent",
        "summarizer_agent",
        "critic_agent",
        "report_writer_agent",
    ]
    assert all(step.status == AgentStepStatus.COMPLETED for step in steps)
    assert all(step.output_payload for step in steps)


def test_day_7_agent_package_imports_after_models_are_registered() -> None:
    assert "agent_steps" in Base.metadata.tables
