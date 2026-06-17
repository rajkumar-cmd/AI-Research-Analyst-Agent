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
    summary: str
    critique: str
    report_markdown: str
    errors: list[str]
