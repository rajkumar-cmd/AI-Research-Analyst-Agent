import math
import re
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from app.vectorstore.chroma import MetadataValue
from app.vectorstore.types import VectorDocument

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class LexicalSearchResult:
    id: str
    text: str
    metadata: dict[str, Any]
    score: float
    matched_terms: list[str] = field(default_factory=list)


class LexicalRetriever:
    def __init__(self) -> None:
        self._documents: dict[str, VectorDocument] = {}
        self._term_frequencies: dict[str, Counter[str]] = {}
        self._document_frequencies: Counter[str] = Counter()

    def index_documents(self, documents: Sequence[VectorDocument]) -> int:
        for document in documents:
            self._remove_document(document.id)
            tokens = _tokenize(document.text)
            term_frequency = Counter(tokens)

            self._documents[document.id] = document
            self._term_frequencies[document.id] = term_frequency
            self._document_frequencies.update(term_frequency.keys())

        return len(documents)

    def search(
        self,
        query: str,
        limit: int = 5,
        where: dict[str, MetadataValue] | None = None,
    ) -> list[LexicalSearchResult]:
        if limit < 1:
            raise ValueError("Search limit must be at least 1.")

        query_terms = _tokenize(query)
        if not query_terms:
            return []

        query_counts = Counter(query_terms)
        results: list[LexicalSearchResult] = []
        document_count = max(len(self._documents), 1)

        for document_id, document in self._documents.items():
            if where and not _metadata_matches(document.metadata, where):
                continue

            term_frequency = self._term_frequencies[document_id]
            matched_terms = sorted(term for term in query_counts if term in term_frequency)
            if not matched_terms:
                continue

            score = 0.0
            document_length = max(sum(term_frequency.values()), 1)
            for term in matched_terms:
                tf = term_frequency[term] / document_length
                idf = math.log((1 + document_count) / (1 + self._document_frequencies[term])) + 1
                score += tf * idf * query_counts[term]

            results.append(
                LexicalSearchResult(
                    id=document.id,
                    text=document.text,
                    metadata=document.metadata,
                    score=score,
                    matched_terms=matched_terms,
                )
            )

        return sorted(results, key=lambda result: (-result.score, result.id))[:limit]

    def _remove_document(self, document_id: str) -> None:
        self._documents.pop(document_id, None)
        previous_terms = self._term_frequencies.pop(document_id, None)
        if previous_terms is None:
            return

        for term in previous_terms:
            self._document_frequencies[term] -= 1
            if self._document_frequencies[term] <= 0:
                del self._document_frequencies[term]


def _tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


def _metadata_matches(metadata: dict[str, Any], where: dict[str, MetadataValue]) -> bool:
    return all(metadata.get(key) == value for key, value in where.items())
