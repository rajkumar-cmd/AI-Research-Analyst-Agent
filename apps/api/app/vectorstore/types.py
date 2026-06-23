from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class VectorDocument:
    id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VectorSearchResult:
    id: str
    text: str
    metadata: dict[str, Any]
    distance: float
    score: float


@dataclass(frozen=True)
class HybridSearchResult:
    id: str
    text: str
    metadata: dict[str, Any]
    score: float
    vector_rank: int | None = None
    lexical_rank: int | None = None
    vector_score: float | None = None
    lexical_score: float | None = None
    matched_terms: list[str] = field(default_factory=list)
