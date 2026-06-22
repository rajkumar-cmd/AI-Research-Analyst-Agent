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
