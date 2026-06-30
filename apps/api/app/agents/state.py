from typing import TypedDict


class ResearchGraphState(TypedDict):
    run_id: str
    user_id: str
    query: str
    quota_allowed: bool
    approval_required: bool
    approval_request_id: str | None
    approval_status: str | None
    plan: list[str]
    research_notes: list[str]
    source_candidates: list[dict[str, object]]
    validated_sources: list[dict[str, object]]
    source_quality_score: float
    summary: str
    critique: str
    report_markdown: str
    errors: list[str]
