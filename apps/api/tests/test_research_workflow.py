from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agents.graph import run_research_workflow
from app.agents.providers import MockLLMProvider
from app.core.database import Base
from app.models.research import AgentStep, AgentStepStatus, ApprovalRequest, ApprovalStatus, ResearchRun, ResearchRunStatus
from app.models.user import User
from app.services.approvals import (
    approve_approval_request,
    reject_approval_request,
    resume_approved_research_workflow,
)


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
        "human_approval",
        "report_writer_agent",
    ]
    assert all(step.status == AgentStepStatus.COMPLETED for step in steps)
    assert all(step.output_payload for step in steps)


def test_research_workflow_pauses_for_human_approval_and_resumes_after_approval(db_session: Session) -> None:
    user, run = _create_research_run(db_session)

    approval_state = run_research_workflow(
        db=db_session,
        run=run,
        provider=MockLLMProvider(),
        require_human_approval=True,
    )

    db_session.refresh(run)
    approval_request = db_session.scalars(select(ApprovalRequest)).one()
    paused_steps = db_session.scalars(select(AgentStep).order_by(AgentStep.started_at)).all()

    assert user.id == run.user_id
    assert run.status == ResearchRunStatus.WAITING_FOR_APPROVAL
    assert run.current_node == "human_approval"
    assert approval_state["approval_request_id"] == approval_request.id
    assert approval_request.status == ApprovalStatus.PENDING
    assert approval_request.draft_payload["summary"]
    assert [step.node_name for step in paused_steps] == [
        "quota_guard",
        "planner_agent",
        "research_agent",
        "summarizer_agent",
        "critic_agent",
        "human_approval",
    ]

    approve_approval_request(
        db=db_session,
        approval_request_id=approval_request.id,
        reviewer_feedback="Looks ready for a draft report.",
    )
    final_state = resume_approved_research_workflow(
        db=db_session,
        approval_request_id=approval_request.id,
        provider=MockLLMProvider(),
    )

    db_session.refresh(run)
    db_session.refresh(approval_request)
    all_steps = db_session.scalars(select(AgentStep).order_by(AgentStep.started_at)).all()

    assert run.status == ResearchRunStatus.COMPLETED
    assert approval_request.status == ApprovalStatus.APPROVED
    assert approval_request.approved_at is not None
    assert "Research Brief" in final_state["report_markdown"]
    assert [step.node_name for step in all_steps][-1] == "report_writer_agent"


def test_rejecting_approval_request_cancels_research_run(db_session: Session) -> None:
    _, run = _create_research_run(db_session, query="Research risky AI vendor claims")
    run_research_workflow(
        db=db_session,
        run=run,
        provider=MockLLMProvider(),
        require_human_approval=True,
    )
    approval_request = db_session.scalars(select(ApprovalRequest)).one()

    reject_approval_request(
        db=db_session,
        approval_request_id=approval_request.id,
        reviewer_feedback="Source confidence is too low.",
    )

    db_session.refresh(run)
    db_session.refresh(approval_request)
    assert approval_request.status == ApprovalStatus.REJECTED
    assert run.status == ResearchRunStatus.CANCELLED
    assert run.error_message == "Source confidence is too low."


def test_day_7_agent_package_imports_after_models_are_registered() -> None:
    assert "agent_steps" in Base.metadata.tables


def _create_research_run(
    db_session: Session,
    query: str = "Research top AI data engineering trends for 2026",
) -> tuple[User, ResearchRun]:
    user = User(
        name="Rajkumar Pradhan",
        email=f"{query.lower().replace(' ', '.')}@example.com",
        password_hash="hashed-password",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    run = ResearchRun(user_id=user.id, query=query)
    db_session.add(run)
    db_session.commit()
    db_session.refresh(run)
    return user, run
