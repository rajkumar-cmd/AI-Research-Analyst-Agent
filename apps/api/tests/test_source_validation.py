from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agents.source_validation import (
    SourceCandidate,
    SourceValidationAgent,
    persist_source_validation_results,
)
from app.models.research import ResearchRun, Source, SourceValidationStatus
from app.models.user import User


def test_source_validation_agent_accepts_trusted_relevant_https_source() -> None:
    validator = SourceValidationAgent()

    result = validator.validate(
        SourceCandidate(
            title="NIST artificial intelligence risk management guidance",
            url="https://www.nist.gov/artificial-intelligence",
            publisher="NIST",
            excerpt="AI risk management guidance for enterprise governance teams.",
        ),
        query="AI risk management guidance",
    )

    assert result.status == SourceValidationStatus.ACCEPTED
    assert result.credibility_score >= 0.72
    assert "Uses secure HTTPS transport." in result.reasons
    assert "guidance" in result.matched_terms


def test_source_validation_agent_rejects_invalid_source_url() -> None:
    validator = SourceValidationAgent()

    result = validator.validate(
        SourceCandidate(
            title="Anonymous claim dump",
            url="not-a-real-url",
            publisher=None,
        ),
        query="AI market claims",
    )

    assert result.status == SourceValidationStatus.REJECTED
    assert result.credibility_score == 0.05


def test_source_validation_results_are_persisted_to_sources(db_session: Session) -> None:
    user = User(name="Rajkumar Pradhan", email="sources@example.com", password_hash="hashed-password")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    run = ResearchRun(user_id=user.id, query="AI data engineering trends")
    db_session.add(run)
    db_session.commit()
    db_session.refresh(run)

    result = SourceValidationAgent().validate(
        SourceCandidate(
            title="arXiv search results for AI data engineering trends",
            url="https://arxiv.org/search/?query=ai-data-engineering&searchtype=all",
            publisher="arXiv",
            excerpt="AI data engineering trend evidence.",
            metadata={"source_type": "academic_search"},
        ),
        query=run.query,
    )
    persist_source_validation_results(db=db_session, run=run, results=[result])
    db_session.commit()

    source = db_session.scalars(select(Source)).one()

    assert source.validation_status == SourceValidationStatus.ACCEPTED
    assert source.credibility_score == Decimal(str(result.credibility_score))
    assert source.metadata_json["source_type"] == "academic_search"
    assert source.metadata_json["matched_terms"]
