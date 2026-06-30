from dataclasses import asdict, dataclass, field
from decimal import Decimal
from typing import Any
from urllib.parse import urlparse

from sqlalchemy.orm import Session

from app.models.research import ResearchRun, Source, SourceValidationStatus

TRUSTED_DOMAINS = {
    "arxiv.org",
    "nist.gov",
    "oecd.org",
    "stanford.edu",
    "mit.edu",
    "mckinsey.com",
}


@dataclass(frozen=True)
class SourceCandidate:
    title: str
    url: str
    publisher: str | None = None
    excerpt: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SourceValidationResult:
    title: str
    url: str
    publisher: str | None
    status: SourceValidationStatus
    credibility_score: float
    reasons: list[str]
    matched_terms: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_state_payload(self) -> dict[str, object]:
        payload = asdict(self)
        payload["status"] = self.status.value
        return payload


class SourceValidationAgent:
    def build_candidates(self, query: str, research_notes: list[str]) -> list[SourceCandidate]:
        topic_slug = "-".join(_ordered_tokens(query)[:6]) or "research"
        supporting_note = research_notes[0] if research_notes else "Preliminary research note unavailable."
        return [
            SourceCandidate(
                title=f"Academic search results for {query}",
                url=f"https://arxiv.org/search/?query={topic_slug}&searchtype=all",
                publisher="arXiv",
                excerpt=supporting_note,
                metadata={"source_type": "academic_search"},
            ),
            SourceCandidate(
                title="NIST artificial intelligence risk and measurement resources",
                url="https://www.nist.gov/artificial-intelligence",
                publisher="NIST",
                excerpt="Government-backed AI risk and measurement guidance for validating research claims.",
                metadata={"source_type": "government_reference"},
            ),
            SourceCandidate(
                title="Unverified market trend blog",
                url=f"http://unverified.example/{topic_slug}",
                publisher="Unknown blog",
                excerpt="Fast-moving commentary without clear source ownership or secure transport.",
                metadata={"source_type": "unverified_commentary"},
            ),
        ]

    def validate_many(
        self,
        candidates: list[SourceCandidate],
        query: str,
    ) -> list[SourceValidationResult]:
        return [self.validate(candidate, query) for candidate in candidates]

    def validate(self, candidate: SourceCandidate, query: str) -> SourceValidationResult:
        parsed_url = urlparse(candidate.url)
        reasons: list[str] = []
        score = 0.2

        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            return SourceValidationResult(
                title=candidate.title,
                url=candidate.url,
                publisher=candidate.publisher,
                status=SourceValidationStatus.REJECTED,
                credibility_score=0.05,
                reasons=["URL is missing a valid scheme or host."],
                matched_terms=[],
                metadata=candidate.metadata,
            )

        if parsed_url.scheme == "https":
            score += 0.2
            reasons.append("Uses secure HTTPS transport.")
        else:
            reasons.append("Uses insecure HTTP transport.")

        domain = parsed_url.netloc.lower().removeprefix("www.")
        if domain in TRUSTED_DOMAINS or any(domain.endswith(f".{trusted}") for trusted in TRUSTED_DOMAINS):
            score += 0.25
            reasons.append("Publisher domain is on the trusted source list.")
        elif candidate.publisher:
            score += 0.08
            reasons.append("Publisher name is present but not yet trusted.")
        else:
            reasons.append("Publisher identity is missing.")

        matched_terms = sorted(_tokens(query) & _tokens(f"{candidate.title} {candidate.excerpt or ''}"))
        if matched_terms:
            score += min(0.25, len(matched_terms) * 0.05)
            reasons.append("Source title or excerpt matches the research query.")
        else:
            reasons.append("No direct query-term overlap found.")

        if len(candidate.title.strip()) >= 20:
            score += 0.08
            reasons.append("Title is descriptive enough for reviewer inspection.")

        score = min(score, 1.0)
        status = _status_for_score(score)
        return SourceValidationResult(
            title=candidate.title,
            url=candidate.url,
            publisher=candidate.publisher,
            status=status,
            credibility_score=round(score, 2),
            reasons=reasons,
            matched_terms=matched_terms,
            metadata=candidate.metadata,
        )


def source_candidates_from_state(candidates: list[dict[str, object]]) -> list[SourceCandidate]:
    return [
        SourceCandidate(
            title=str(candidate.get("title", "Untitled source")),
            url=str(candidate.get("url", "")),
            publisher=_optional_str(candidate.get("publisher")),
            excerpt=_optional_str(candidate.get("excerpt")),
            metadata=_metadata_dict(candidate.get("metadata")),
        )
        for candidate in candidates
    ]


def persist_source_validation_results(
    db: Session,
    run: ResearchRun,
    results: list[SourceValidationResult],
) -> None:
    for result in results:
        db.add(
            Source(
                run_id=run.id,
                title=result.title,
                url=result.url,
                publisher=result.publisher,
                credibility_score=Decimal(str(result.credibility_score)),
                validation_status=result.status,
                metadata_json={
                    "reasons": result.reasons,
                    "matched_terms": result.matched_terms,
                    **result.metadata,
                },
            )
        )
    db.flush()


def _status_for_score(score: float) -> SourceValidationStatus:
    if score >= 0.72:
        return SourceValidationStatus.ACCEPTED
    if score >= 0.45:
        return SourceValidationStatus.WARNING
    return SourceValidationStatus.REJECTED


def _tokens(text: str) -> set[str]:
    return {token for token in text.lower().replace("-", " ").split() if len(token) >= 3}


def _ordered_tokens(text: str) -> list[str]:
    seen: set[str] = set()
    tokens: list[str] = []
    for token in text.lower().replace("-", " ").split():
        if len(token) < 3 or token in seen:
            continue
        seen.add(token)
        tokens.append(token)
    return tokens


def _optional_str(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _metadata_dict(value: object) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}
