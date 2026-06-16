from app.agents.providers import LLMProvider
from app.agents.state import ResearchGraphState


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


def summarizer_node(state: ResearchGraphState, provider: LLMProvider) -> dict[str, object]:
    return {"summary": provider.summarize(state["query"], state["research_notes"])}


def critic_node(state: ResearchGraphState, provider: LLMProvider) -> dict[str, object]:
    return {"critique": provider.critique(state["summary"])}


def report_writer_node(state: ResearchGraphState, provider: LLMProvider) -> dict[str, object]:
    return {
        "report_markdown": provider.write_report(
            query=state["query"],
            summary=state["summary"],
            critique=state["critique"],
        )
    }
