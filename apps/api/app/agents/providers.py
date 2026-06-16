from typing import Protocol


class LLMProvider(Protocol):
    def plan(self, query: str) -> list[str]:
        pass

    def research(self, query: str, plan: list[str]) -> list[str]:
        pass

    def summarize(self, query: str, research_notes: list[str]) -> str:
        pass

    def critique(self, summary: str) -> str:
        pass

    def write_report(self, query: str, summary: str, critique: str) -> str:
        pass


class MockLLMProvider:
    """Deterministic provider for local development and workflow tests."""

    def plan(self, query: str) -> list[str]:
        return [
            f"Clarify the research scope for: {query}",
            "Identify credible source categories and market signals.",
            "Extract trends, risks, recommendations, and open questions.",
        ]

    def research(self, query: str, plan: list[str]) -> list[str]:
        return [
            f"Research note for '{query}': demand is rising across enterprise AI workflows.",
            f"Research note for '{query}': credible analysis should compare adoption, cost, and governance.",
            f"Plan coverage: {len(plan)} investigation steps are ready for deeper retrieval.",
        ]

    def summarize(self, query: str, research_notes: list[str]) -> str:
        return (
            f"{query} shows strong momentum, but the final answer should separate durable trends "
            f"from hype. {len(research_notes)} preliminary notes were synthesized."
        )

    def critique(self, summary: str) -> str:
        return (
            "The draft is directionally useful, but it needs source validation, citations, "
            "and confidence scoring before being treated as a production report."
        )

    def write_report(self, query: str, summary: str, critique: str) -> str:
        return "\n\n".join(
            [
                f"# Research Brief: {query}",
                "## Executive Summary",
                summary,
                "## Critic Notes",
                critique,
                "## Next Steps",
                "- Run hybrid retrieval against trusted sources.",
                "- Validate sources and attach citations.",
                "- Request human approval before publishing.",
            ]
        )
