from typing import TypedDict


class ResearchGraphState(TypedDict):
    run_id: str
    user_id: str
    query: str
    quota_allowed: bool
    plan: list[str]
    research_notes: list[str]
    summary: str
    critique: str
    report_markdown: str
    errors: list[str]
